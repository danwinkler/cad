import math
import pathlib
import random
import subprocess
from dataclasses import dataclass

import cv2
import euclid3
import numpy as np
import shapelysmooth
import solid
import svgpath2mpl
import ziafont
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

import cad.common
from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)


class FontRenderer:
    def __init__(self, path: pathlib.Path):
        self.ziafont = ziafont.font.Font(path.resolve())

    def render(self, text: str, font_scale=1):
        """
        Currently this only works for single characters, as I don't have a good way to determine whic
        """

        polys = []
        cur_x = 0
        kerning = 1 * font_scale
        words = text.split(" ")
        for word in words:
            for letter in word:
                font_text = self.ziafont.text(letter)
                s = font_text.svgxml()
                svg_symbols = s.findall("symbol")
                for symbol in svg_symbols:
                    poly = self.symbol_to_polygon(symbol, font_scale)
                    poly = scale(poly, xfact=1, yfact=-1, origin=(0, 0))
                    poly = translate(poly, xoff=cur_x, yoff=0)
                    polys.append(poly)
                    cur_x += poly.bounds[2] - poly.bounds[0] + kerning

            cur_x += kerning * 3

        return unary_union(polys)

    def symbol_to_polygon(self, symbol, font_scale):
        svg_paths = symbol.findall("path")
        polys = []
        for svg_path in svg_paths:
            path = svgpath2mpl.parse_path(svg_path.attrib["d"])

            path.vertices = path.vertices * font_scale

            for mpl_poly in path.to_polygons(closed_only=False):
                poly = Polygon(mpl_poly)
                polys.append(poly)

        for i in range(len(polys)):
            for j in range(i + 1, len(polys)):
                a = polys[i]
                b = polys[j]

                if not a or not b:
                    continue

                if a.contains(b):
                    polys[i] = a - b
                    polys[j] = None

        return unary_union([p for p in polys if p])


def arc(start_angle, end_angle, radius, center=(0, 0)):
    num_points = 100
    points = []
    for i in range(num_points + 1):
        angle = start_angle + (end_angle - start_angle) * i / num_points
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        points.append((x, y))
    return LineString(points)


class Sign:
    def __init__(self, texts):
        self.texts = texts

    def get_multi_model(self):
        model = MultipartModel(5)

        model.perimeter_bounds = (0, 0, 580, 275)

        font_scale = 2
        hole_height = 12

        for text_i, text in enumerate(self.texts):
            svgfont = FontRenderer(
                pathlib.Path(__file__).parent / "../../../common/Roboto-Regular.ttf"
            )

            sign_model = Model()

            text_poly = scale(
                svgfont.render(text, font_scale=font_scale * 10),
                xfact=0.1,
                yfact=0.1,
                origin=(0, 0),
            )

            sign_model.add_poly(text_poly, layer="text").color(0.8, 0.1, 0.1).translate(
                0, 0, 1
            )

            buffer = 20
            round = 12

            box_extra = buffer - round
            sign_outline = box(
                text_poly.bounds[0] - box_extra,
                -box_extra,
                text_poly.bounds[2] + box_extra,
                8 * font_scale + box_extra,
            )

            sign_outline = sign_outline.buffer(round)

            # Make holes
            center = (sign_outline.bounds[0] + sign_outline.bounds[2]) / 2
            hole_x_off = 30
            hole_y_off = 30
            hole = box(0, 0, model.default_thickness + 1, hole_height)

            holes = unary_union(
                [
                    translate(hole, xoff=center - hole_x_off, yoff=hole_y_off),
                    translate(hole, xoff=center + hole_x_off, yoff=hole_y_off),
                ]
            )

            sign_outline = unary_union([sign_outline, holes.buffer(5)])
            sign_outline -= holes

            sign_model.add_poly(sign_outline)

            model.add_model(sign_model).renderer.translate(y=100 * text_i)

            # Hanger
            wood_width = 18
            hanger_width = 12
            hook_width = hole_height - 2
            arc_rad = 30
            hanger = [
                box(0, 0, hanger_width * 2 + wood_width, hanger_width),
                box(0, 0, hanger_width, 40),
                translate(box(0, 0, hanger_width, 60), xoff=hanger_width + wood_width),
                arc(
                    45,
                    90,
                    arc_rad,
                    center=(
                        hanger_width * 2 + wood_width,
                        60 - arc_rad - hook_width / 2,
                    ),
                ).buffer(hook_width / 2),
            ]

            hanger = unary_union(hanger)

            for i in range(2):
                hanger_model = Model()
                hanger_model.add_poly(hanger)

                model.add_model(hanger_model).renderer.translate(
                    x=200 + i * 80, y=100 * text_i
                )

        return model


texts = [
    "Big Rainbow",
    "Red Cherry",
    "Patio",
    "San Marzano",
    "Sungold",
]

texts = texts[0:][:1]

m = Sign(texts)

model = m.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
# model.render_parts(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
