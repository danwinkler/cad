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
from shapely import concave_hull, intersection
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


class Walls:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_multi_model(self):
        model = MultipartModel(5)

        model.perimeter_bounds = (0, 0, 580, 275)

        n_sections = math.ceil(self.width / model.perimeter_bounds[2])
        section_width = self.width / n_sections
        section_height = 250

        m = Model()

        poly = box(0, 0, section_width, section_height)

        inner_ring_offset = 40

        circle_xfact = (section_width / 2) / (section_height)

        poly -= scale(
            Point(section_width / 2, 0).buffer(section_height - inner_ring_offset),
            xfact=circle_xfact,
            yfact=1,
        )

        outline = poly

        poly -= poly.buffer(-5)

        internal_structure = []
        n_steps = 60
        for i in range(100):
            angle = i * math.pi / n_steps
            internal_structure.append(
                LineString(
                    [
                        (section_width / 2, 0),
                        (
                            section_width / 2 + math.cos(angle) * 500,
                            math.sin(angle) * 500,
                        ),
                    ]
                ).buffer(2)
            )

        for i in range(1, 10):
            circle = scale(
                Point(section_width / 2, 0).buffer(
                    section_height - inner_ring_offset + i * 15
                ),
                xfact=circle_xfact,
                yfact=1,
            )

            internal_structure.append(circle.buffer(4) - circle)

        poly = unary_union(
            [
                intersection(unary_union(internal_structure), outline),
                poly,
            ]
        )

        tab_positions = [
            section_height - 30,
            section_height - 60,
        ]

        tab_x_offset = 10

        tab_width = 10
        tab_height = 5 - 0.2  # 0.2 is the kerf

        for tab_y in tab_positions:
            tab = unary_union(
                [
                    box(
                        tab_x_offset,
                        tab_y,
                        tab_x_offset + tab_width,
                        tab_y + tab_height,
                    ),
                    box(
                        section_width - tab_x_offset - tab_width,
                        tab_y,
                        section_width - tab_x_offset,
                        tab_y + tab_height,
                    ),
                ]
            )

            poly = unary_union([tab.buffer(10), poly])

            poly -= tab

        m.add_poly(poly)

        model.add_model(m)

        return model


m = Walls(1111, 431)

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
