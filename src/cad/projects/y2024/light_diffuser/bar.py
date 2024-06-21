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
        self.segment_height = 3.3 * in_to_mm
        self.circle_rad = 1.5

        print(f"Segment Length: {self.segment_length}")

    def make_panel(self, seed, circle_rad=2, x_offset=0):
        random.seed(seed)

        m = Model()

        panel = box(0, 0, self.segment_length, self.segment_height)

        margin_x = self.circle_rad + 5
        margin_top = 0.75 * in_to_mm
        margin_bottom = 10

        index = rtree.index.Index()
        points = []
        for i in tqdm(range(3000)):
            x = random.uniform(margin_x, self.segment_length - margin_x)
            y = random.uniform(margin_bottom, self.segment_height - margin_top)

            min_dist = 5 + math.sin((x + x_offset - y * 1.2) * 0.05) * 1.5

            nearest = list(index.nearest((x, y), 1))

            if len(nearest) == 1:
                nearest_x = points[nearest[0]][0]
                nearest_y = points[nearest[0]][1]
                dist_sq = (x - nearest_x) ** 2 + (y - nearest_y) ** 2

                if dist_sq < min_dist**2:
                    continue

            points.append((x, y))
            index.insert(len(points) - 1, (x, y, x, y))

        panel = panel - unary_union([Point(x, y).buffer(circle_rad) for x, y in points])

        m.add_poly(panel)

        return m

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 580, 295)

        for i in range(3):
            model.add_model(
                self.make_panel(0, self.circle_rad, x_offset=i * self.segment_length)
            ).renderer.translate(x=i * self.segment_length)

        return model


m = Diffuser()

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
