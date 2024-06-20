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

        print(f"Segment Length: {self.segment_length}")

    def make_hook(self):
        m = Model()

        hook_depth = 4.0 * in_to_mm
        inner_corner_rad = 20
        middle_size = 1.5 * in_to_mm

        hook = (
            unary_union(
                [
                    box(
                        0,
                        self.expand_rad,
                        hook_depth + self.hook_leg_width,
                        middle_size + (self.hook_leg_width) * 2 - self.expand_rad,
                    ),
                    Point(0, middle_size / 2 + self.hook_leg_width).buffer(
                        2.8 * in_to_mm / 2
                    ),
                ]
            )
            .buffer(self.expand_rad + inner_corner_rad)
            .buffer(-inner_corner_rad)
        )

        # cutouts for cross bar
        cutout_x = hook_depth - 20
        cutout = box(
            cutout_x,
            middle_size + self.hook_leg_width * 2 - 5,
            cutout_x + 4.8,
            middle_size + self.hook_leg_width * 2,
        )

        hook = hook - unary_union(
            [
                hook.buffer(-self.hook_leg_width),
                box(hook_depth, 0, hook_depth + 2 * in_to_mm, 3 * in_to_mm),
                cutout,
            ]
        )

        m.add_poly(hook)

        return m

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 580, 295)

        model.add_model(self.make_hook())

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
