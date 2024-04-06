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
        font_text = self.ziafont.text(text)
        s = font_text.svgxml()
        svg_paths = s.find("symbol").findall("path")
        polys = []
        for svg_path in svg_paths:
            sub_polys = []
            path = svgpath2mpl.parse_path(svg_path.attrib["d"])

            path.vertices = path.vertices * font_scale

            for mpl_poly in path.to_polygons(closed_only=False):
                poly = Polygon(mpl_poly)
                sub_polys.append(poly)

            if len(sub_polys) == 0:
                continue
            elif len(sub_polys) == 1:
                polys.append(sub_polys[0])
            else:
                polys.append(sub_polys[0] - unary_union(sub_polys[1:]))
            # polygons = path.to_polygons()
            # # Convert to shapely

            # for poly in polygons:
            #     polys.append(Polygon(poly))
        return unary_union(polys)


def find_max_y_at_x(polygon, x):
    """
    Given a Shapely polygon and an x-coordinate,
    returns the largest y-value on the polygon's boundary for that x-coordinate.
    """
    if not polygon.is_valid or polygon.is_empty:
        raise ValueError("Invalid polygon provided.")

    max_y = None
    exterior = polygon.exterior

    if exterior is None:
        return None

    coords = list(exterior.coords)

    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]

        # Check if the segment is vertical
        if x1 == x2:
            if x1 == x:
                # The x coordinate lies exactly on a vertical line segment
                candidate_y = max(y1, y2)
                if max_y is None or candidate_y > max_y:
                    max_y = candidate_y
        else:
            # Check if the x coordinate is between the x values of the segment
            if min(x1, x2) <= x <= max(x1, x2):
                # Linear interpolation to find the y value
                y = y1 + (y2 - y1) * ((x - x1) / (x2 - x1))
                if max_y is None or y > max_y:
                    max_y = y

    return max_y


def save_mask(text_poly: MultiPolygon, letter):
    # Translate the text polygon such that the lower left corner is at the origin
    text_poly = translate(
        text_poly, xoff=-text_poly.bounds[0], yoff=-text_poly.bounds[1]
    )

    letter_mask_folder = pathlib.Path(__file__).parent / "letter_masks"
    letter_mask_folder.mkdir(exist_ok=True)

    mask_size = 512
    mask_margin = 64
    shape_size = mask_size - mask_margin * 2

    # Resize the text polygon to fit within the mask, but maintain aspect ratio
    resize_factor = shape_size / max(
        text_poly.bounds[2] - text_poly.bounds[0],
        text_poly.bounds[3] - text_poly.bounds[1],
    )

    resized_text_poly = translate(
        scale(
            text_poly,
            xfact=resize_factor,
            yfact=-resize_factor,
            origin=(0, 0),
        ),
        xoff=mask_margin,
        yoff=mask_margin + shape_size,
    )

    image = np.zeros((mask_size, mask_size, 3), dtype=np.uint8)
    int_coords = lambda x: np.array(x).round().astype(np.int32)
    exterior = int_coords(resized_text_poly.exterior.coords)
    interiors = [
        int_coords(interior.coords) for interior in resized_text_poly.interiors
    ]

    cv2.fillPoly(image, [exterior], (255, 255, 255))
    if len(interiors) > 0:
        cv2.fillPoly(image, interiors, (0, 0, 0))

    cv2.imwrite((letter_mask_folder / f"{letter}.png").resolve().as_posix(), image)


class Letters:
    def get_multi_model(self):
        model = MultipartModel(5)

        model.perimeter_bounds = (0, 0, 580, 275)

        text_scale = 1
        font_scale = 10
        ring_outer_rad = 6
        ring_inner_rad = 3

        text = "HAPPY BIRTHDAY ZOE"
        # text = "TEST"
        # text = "BCD"

        double_ring_letters = "HY"

        svgfont = FontRenderer(pathlib.Path(__file__).parent / "Roboto-Black.otf")

        for i, c in enumerate(text):
            if c == " ":
                continue

            character_model = Model()

            text_poly = scale(
                svgfont.render(c, font_scale=font_scale),
                xfact=text_scale,
                yfact=-text_scale,
                origin=(0, 0),
            )

            text_poly = translate(
                text_poly,
                xoff=-text_poly.bounds[0],
                yoff=-text_poly.bounds[1],
            )

            # save_mask(text_poly, c)

            if c in double_ring_letters:
                x_positions = [
                    text_poly.bounds[0] + ring_outer_rad,
                    text_poly.bounds[2] - ring_outer_rad,
                ]
                for x in x_positions:
                    midpoint_y = find_max_y_at_x(text_poly, x)

                    ring = translate(
                        Point(x, midpoint_y).buffer(ring_outer_rad)
                        - Point(x, midpoint_y).buffer(ring_inner_rad),
                        yoff=ring_inner_rad,
                    )

                    text_poly = unary_union([text_poly, ring])
            else:
                midpoint_x = text_poly.centroid.x
                midpoint_y = find_max_y_at_x(text_poly, midpoint_x)

                ring = translate(
                    Point(midpoint_x, midpoint_y).buffer(ring_outer_rad)
                    - Point(midpoint_x, midpoint_y).buffer(ring_inner_rad),
                    yoff=ring_inner_rad,
                )

                text_poly = unary_union([text_poly, ring])

            # Something is wrong with the packing algorithm
            text_poly = rotate(text_poly, 90)

            character_model.add_poly(text_poly)

            model.add_model(character_model).renderer.translate(i * 100, 0)

        return model


m = Letters()

model = m.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
model.render_parts(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
