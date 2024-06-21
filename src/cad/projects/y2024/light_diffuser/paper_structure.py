import math
import pathlib
import random
import subprocess
from dataclasses import dataclass

import cv2
import euclid3
import numpy as np
import rtree
import shapelysmooth
import solid
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils
from tqdm import tqdm

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    SolidModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)
from cad.common.project_step import ProjectSteps

in_to_mm = 25.4


class Diffuser:
    def __init__(
        self,
    ):
        self.segment_length = 4 * 12 * in_to_mm / 3
        self.circle_rad = 1.5
        self.hook_leg_width = 10
        self.expand_rad = 5

        self.middle_size = 1.5 * in_to_mm

        self.hook_depth = 3.0 * in_to_mm
        self.hook_cutout_x = self.hook_depth - 20

        self.cutout_wood_width = 4.8

        self.support_length = 8 * in_to_mm
        self.support_locations = [
            10,
            self.support_length / 2 - self.cutout_wood_width / 2,
            self.support_length - 10 - self.cutout_wood_width,
        ]

        print(f"Segment Length: {self.segment_length}")

    def make_hook(self):
        m = Model()

        inner_corner_rad = 20

        hook = (
            unary_union(
                [
                    box(
                        0,
                        self.expand_rad,
                        self.hook_depth + self.hook_leg_width,
                        self.middle_size + (self.hook_leg_width) * 2 - self.expand_rad,
                    ),
                    Point(0, self.middle_size / 2 + self.hook_leg_width).buffer(
                        2.8 * in_to_mm / 2
                    ),
                ]
            )
            .buffer(self.expand_rad + inner_corner_rad)
            .buffer(-inner_corner_rad)
        )

        # cutouts for cross bar

        cutout = box(
            self.hook_cutout_x,
            self.middle_size + self.hook_leg_width * 2 - 5,
            self.hook_cutout_x + self.cutout_wood_width,
            self.middle_size + self.hook_leg_width * 2,
        )

        # Cut out interior and right side
        hook = hook - unary_union(
            [
                hook.buffer(-self.hook_leg_width),
                box(self.hook_depth, -1, self.hook_depth + 2 * in_to_mm, 3 * in_to_mm),
                cutout,
            ]
        )

        m.add_poly(hook)

        return m

    def make_cross_bar(self):
        poly = box(0, 0, self.support_length, self.hook_leg_width)
        for x in self.support_locations:
            poly = poly - box(x, -1, x + self.cutout_wood_width, 5)

        m = Model()

        m.add_poly(poly)

        return m

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 580, 295)

        for i in self.support_locations:
            model.add_model(self.make_hook()).renderer.rotate(
                a=90, v=(1, 0, 0)
            ).translate(y=i + self.cutout_wood_width)

        model.add_model(self.make_cross_bar()).renderer.rotate(
            a=90, v=(1, 0, 0)
        ).rotate(a=90, v=(0, 0, 1)).translate(
            x=self.hook_cutout_x, z=self.middle_size + self.hook_leg_width
        )

        return model


m = Diffuser()

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
