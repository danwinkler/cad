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
    s_poly_to_scad,
    skeleton_to_polys,
)

# from cad.common.helper import *


# random.seed(0)


class DiamondPattern:
    def __init__(
        self,
        n_rows,
        diamond_height,
        diamond_width,
        diamond_y_spacing,
        diamond_x_spacing,
        center,
        n_offset=2,
    ):
        self.n_rows = n_rows
        self.diamond_height = diamond_height
        self.diamond_width = diamond_width
        self.diamond_y_spacing = diamond_y_spacing
        self.diamond_x_spacing = diamond_x_spacing
        self.center = center
        self.n_offset = n_offset

    def get(self):
        diamonds = []
        start_x = (
            self.center.x
            - (self.diamond_width + self.diamond_x_spacing) * self.n_rows * 0.5
        )
        for i in range(self.n_rows):
            for j in range(-self.n_offset, self.n_offset + 1):
                y = self.center.y + j * (self.diamond_height + self.diamond_y_spacing)
                if i % 2 == 0:
                    y += (self.diamond_height + self.diamond_y_spacing) / 2

                x = start_x + i * (self.diamond_width + self.diamond_x_spacing)

                diamond = Polygon(
                    [
                        (x, y),
                        (x + self.diamond_width / 2, y + self.diamond_height / 2),
                        (x + self.diamond_width, y),
                        (x + self.diamond_width / 2, y - self.diamond_height / 2),
                    ]
                )

                diamonds.append(diamond)
        return unary_union(diamonds)


class Lantern:
    def __init__(self):
        # Global settings
        self.wood_thickness = 5

        # Bend shape settings
        self.bend_shape_height = 100
        self.bend_radius = 20
        self.side_length = 50
        self.bend_length = math.pi * self.bend_radius / 2
        self.tab_length = 10

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def get_bend_shape(self):
        shape = box(
            self.bend_radius,
            self.bend_radius,
            self.bend_radius + self.side_length,
            self.bend_radius + self.side_length,
        ).buffer(self.bend_radius)

        return shape

    def get_perimeter_length(self):
        return (self.side_length + self.bend_length) * 4

    def get_bendy_model(self):
        m = Model()

        total_x_offset = self.tab_length / 2 + 20

        def make_wave(y_scale, y_offset, size, blur=51):
            n_segments = 100

            def phase(x):
                offset = (
                    self.bend_length / (self.side_length + self.bend_length)
                ) * math.pi
                return math.cos(
                    x * 2 * math.pi / self.get_perimeter_length() * 4 + offset
                )

            points = []
            for i in range(-20, n_segments + 20):
                x = i * self.get_perimeter_length() / n_segments
                y = (
                    phase(x) * self.bend_shape_height * y_scale
                    + self.bend_shape_height * y_offset
                )
                points.append((x, y, size))

            lines = []
            for i in range(1, len(points)):
                p1 = points[i - 1]
                p2 = points[i]

                lines.append((p1, p2))

            polys = skeleton_to_polys(
                lines,
                im_scale=2,
                blur=blur,
                margin=blur // 2 + 1,
                debug_image=False,
            )

            polys = [shapelysmooth.taubin_smooth(p) for p in polys]

            return unary_union(polys)

        outline = box(0, 0, self.get_perimeter_length(), self.bend_shape_height)

        big = unary_union(
            [
                make_wave(0.25, 0.25, 14000, blur=61),
                make_wave(-0.25, 0.75, 14000, blur=61),
            ]
        )

        small = unary_union(
            [
                make_wave(-0.25, 0.25, 1500),
                make_wave(0.25, 0.75, 1500),
            ]
        )

        small = small.intersection(Polygon(big.exterior))

        shape = unary_union(
            [
                big,
                small,
            ]
        )

        for i in range(-1, 5):
            diamond_width = 1.5
            diamond_x_spacing = 0.8
            n_rows = int(self.bend_length / (diamond_width + diamond_x_spacing)) + 1
            dp = DiamondPattern(
                n_rows=n_rows,
                diamond_height=20,
                diamond_width=diamond_width,
                diamond_y_spacing=3,
                diamond_x_spacing=diamond_x_spacing,
                center=Point(
                    (self.side_length + self.bend_length) * i
                    + self.side_length
                    + self.bend_length * 0.5,
                    self.bend_shape_height * 0.5,
                ),
                n_offset=4,
            )

            shape = shape.difference(dp.get())

        shape = translate(shape, total_x_offset)

        shape = shape.intersection(outline)

        bend_shape = self.get_bend_shape()

        m.add_poly(shape, BendyRenderer(bend_shape, x_offset=total_x_offset))

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        model.add_model(self.get_bendy_model())

        return model


lantern = Lantern()

model = lantern.get_multi_model()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
model.render_dxfs(output_dir)

top_level_geom = model.render_full()

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
