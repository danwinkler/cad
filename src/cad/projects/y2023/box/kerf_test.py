"""
Did three tests, with laser settings:
Material Thickness: 5mm
Power: 100%
Speed: 13mm/s
Power and Speed were default for the 6mm basswood setting (I'm using 5mm birch)

Results:
.125 - not terrible, but a little loose. Would glue up just fine.
.11 - Nice snap fit.
.1 - Possible to pre
"""

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
    BendyRenderer,
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)


class KerfTest:
    def __init__(self, kerf_adjustment):
        self.kerf_adjustment = kerf_adjustment
        self.tab_width = 10
        self.width = 60
        self.depth = 20
        self.wood_thickness = 4.9

    def piece(self, offset=False):
        m = Model(thickness=self.wood_thickness)

        shape = box(0, 0, self.width, self.depth)

        start_x = self.tab_width if offset else 0
        x = start_x
        while x < self.width:
            start_adjustment = self.kerf_adjustment if x > 0 else 0
            end_adjustment = (
                self.kerf_adjustment if x < self.width - self.tab_width else 0
            )
            shape = shape.difference(
                box(
                    x + start_adjustment,
                    self.depth - self.wood_thickness,
                    x + self.tab_width - end_adjustment,
                    self.depth,
                )
            )
            x += self.tab_width * 2

        m.add_poly(shape)

        lines = [
            f"Kerf Test {'B' if offset else 'A'} - thickness: {self.wood_thickness}",
            f"kerf adjustment: {self.kerf_adjustment}",
        ]

        text_scale = 0.002
        for i, line in enumerate(lines):
            text_shape = scale(
                get_text_polygon(line), text_scale, text_scale, origin=(0, 0)
            )
            text_shape = translate(
                text_shape, 3, self.depth - self.wood_thickness - 5 - 7 * i
            )
            m.add_poly(text_shape, layer="text").color(0.9, 0.2, 0.2).thickness(
                self.wood_thickness + 0.1
            )

        return m

    def get_model(self):
        m = MultipartModel(self.wood_thickness)

        m.add_model(self.piece())
        m.add_model(self.piece(True)).renderer.rotate(-90, [1, 0, 0]).translate(
            0, self.depth - self.wood_thickness, self.depth
        ).color(0.7, 0.6, 0.4)

        return m


kerf_test = KerfTest(0.11)

model = kerf_test.get_model()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
model.render_dxfs(output_dir)

top_level_geom = model.render_full()

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
