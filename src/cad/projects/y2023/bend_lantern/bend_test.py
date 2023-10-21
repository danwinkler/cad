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
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)

# from cad.common.helper import *


# random.seed(0)


class Structure:
    def __init__(self):
        # Global settings
        self.wood_thickness = 5
        self.tab_width = 10
        self.n_rows = 18
        self.diamond_height = 22
        self.diamond_width = 1.5
        self.diamond_y_spacing = 3
        self.diamond_x_spacing = 0.8
        self.margin = 20

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def center_section_width(self):
        return self.n_rows * (self.diamond_width + self.diamond_x_spacing)

    def total_width(self):
        return self.center_section_width() + 2 * self.margin

    def bend_test_model(
        self,
    ):
        m = Model()

        main = box(0, 0, self.total_width(), 50)

        start = Point(self.margin, 25)

        for i in range(self.n_rows):
            for j in range(-2, 3):
                y = start.y + j * (self.diamond_height + self.diamond_y_spacing)
                if i % 2 == 0:
                    y += (self.diamond_height + self.diamond_y_spacing) / 2

                x = start.x + i * (self.diamond_width + self.diamond_x_spacing)

                diamond = Polygon(
                    [
                        (x, y),
                        (x + self.diamond_width / 2, y + self.diamond_height / 2),
                        (x + self.diamond_width, y),
                        (x + self.diamond_width / 2, y - self.diamond_height / 2),
                    ]
                )

                main = main.difference(diamond)

        main = unary_union(
            [
                main,
                box(0, -self.wood_thickness, self.tab_width, 0),
                box(
                    self.total_width() - self.tab_width,
                    -self.wood_thickness,
                    self.total_width(),
                    0,
                ),
            ]
        )

        m.add_poly(main)

        return m

    def bottom_model(self, wood_thickness_curve_offset_factor=0):
        m = Model()

        tab_0 = box(-self.tab_width, -self.wood_thickness_tab_hole_size(), 0, 0)

        quarter_circumference = self.center_section_width()
        radius = quarter_circumference / (math.pi * 0.5)

        tab_1_x = (
            (self.margin - self.tab_width)
            + radius
            - wood_thickness_curve_offset_factor * self.wood_thickness
        )
        tab_1_y = (
            (self.margin - self.tab_width)
            + radius
            - wood_thickness_curve_offset_factor * self.wood_thickness
        )

        tab_1 = box(
            tab_1_x,
            tab_1_y,
            tab_1_x + self.wood_thickness_tab_hole_size(),
            tab_1_y + self.tab_width,
        )

        holes = unary_union([tab_0, tab_1])

        outline = Polygon(holes.convex_hull.boundary).buffer(3)

        part = outline - holes

        m.add_poly(part)

        text_scale = 0.002
        text = translate(
            scale(
                get_text_polygon(f"{wood_thickness_curve_offset_factor}"),
                text_scale,
                text_scale,
                text_scale,
                origin=(0, 0),
            ),
            10,
            10,
        )

        m.add_poly(text, layer="text")

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        model.add_model(self.bend_test_model())

        for i, v in enumerate([0, 0.5, 1]):
            bottom = self.bottom_model(wood_thickness_curve_offset_factor=v)
            bottom.translate = (100 + i * 50, 0)
            model.add_model(bottom)

        return model


structure = Structure()

model = structure.get_multi_model()

top_level_geom = model.render_full()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
model.render_dxfs(output_dir)
# model.render_svgs(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
