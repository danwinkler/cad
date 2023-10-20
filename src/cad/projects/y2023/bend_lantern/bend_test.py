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
from cad.common.lasercut import Model, MultipartModel, s_poly_to_scad, skeleton_to_polys

# from cad.common.helper import *


# random.seed(0)


class Structure:
    def __init__(self):
        # Global settings
        self.wood_thickness = 5

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def bend_test_model(
        self,
        n_rows=15,
        diamond_height=22,
        diamond_width=1,
        diamond_y_spacing=3,
        diamond_x_spacing=1,
    ):
        m = Model()

        margin = 20
        center_section_width = n_rows * (diamond_width + diamond_x_spacing)
        total_width = center_section_width + 2 * margin

        main = box(0, 0, total_width, 50)

        start = Point(margin, 25)

        for i in range(n_rows):
            for j in range(-2, 3):
                y = start.y + j * (diamond_height + diamond_y_spacing)
                if i % 2 == 0:
                    y += diamond_height / 2

                x = start.x + i * (diamond_width + diamond_x_spacing)

                diamond = Polygon(
                    [
                        (x, y),
                        (x + diamond_width / 2, y + diamond_height / 2),
                        (x + diamond_width, y),
                        (x + diamond_width / 2, y - diamond_height / 2),
                    ]
                )

                main = main.difference(diamond)

        m.add_poly(main)

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        bend_settings = [
            {},
            {"diamond_height": 44},
            {"diamond_width": 2},
            {"diamond_width": 2, "diamond_height": 44},
        ]

        for i, settings in enumerate(bend_settings):
            m = self.bend_test_model(**settings)
            m.translate = (0, i * 60)
            model.add_model(m)

        return model


structure = Structure()

model = structure.get_multi_model()

top_level_geom = model.render_full()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
model.render_dxfs(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
