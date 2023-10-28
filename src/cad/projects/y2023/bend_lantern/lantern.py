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
        self.bend_shape_height = 200
        self.bend_radius = 40
        self.side_length = 100
        self.bend_length = math.pi * self.bend_radius / 2
        self.tab_length = 8
        self.tab_offset_from_center = 5

        # Base plate settings
        self.base_plate_margin = 20

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def get_bend_shape(self):
        shape = box(
            -self.side_length * 0.5,
            -self.side_length * 0.5,
            self.side_length * 0.5,
            self.side_length * 0.5,
        ).buffer(self.bend_radius)

        return shape

    def get_perimeter_length(self):
        return (self.side_length + self.bend_length) * 4

    def get_bendy_model(self):
        m = Model()

        total_x_offset = self.side_length / 2 + self.bend_length

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
            for i in range(-40, n_segments + 20):
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
                make_wave(0.25, 0.25, 14000, blur=101),
                make_wave(-0.25, 0.75, 14000, blur=101),
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

        for i in range(-1, 5):
            x = (
                (self.side_length + self.bend_length) * i
                + self.side_length * 0.5
                + total_x_offset
            )
            shape = unary_union(
                [
                    shape,
                    # Bottom right
                    box(
                        x + self.tab_offset_from_center,
                        -self.wood_thickness,
                        x + self.tab_offset_from_center + self.tab_length,
                        0,
                    ),
                    # Bottom left
                    box(
                        x - self.tab_offset_from_center - self.tab_length,
                        -self.wood_thickness,
                        x - self.tab_offset_from_center,
                        0,
                    ),
                    # Top right
                    box(
                        x + self.tab_offset_from_center,
                        self.bend_shape_height,
                        x + self.tab_offset_from_center + self.tab_length,
                        self.bend_shape_height + self.wood_thickness,
                    ),
                    # Top left
                    box(
                        x - self.tab_offset_from_center - self.tab_length,
                        self.bend_shape_height,
                        x - self.tab_offset_from_center,
                        self.bend_shape_height + self.wood_thickness,
                    ),
                ]
            )

        # Finally one final intersection (mostly for the x axis) to get rid of any tabs we put on either side
        tab_outline = box(
            0,
            -self.wood_thickness,
            self.get_perimeter_length(),
            self.bend_shape_height + self.wood_thickness,
        )
        shape = shape.intersection(tab_outline)

        bend_shape = self.get_bend_shape()

        m.add_poly(shape, BendyRenderer(bend_shape, x_offset=total_x_offset))

        # m.add_poly(shape).translate(y=-self.bend_shape_height)

        return m

    def get_base_plate_model(self):
        m = Model()

        base_plate_radius = 40

        side_dim = (
            self.side_length
            + self.bend_radius * 2
            + self.base_plate_margin * 2
            - base_plate_radius * 2
        )
        shape = box(
            -side_dim * 0.5,
            -side_dim * 0.5,
            side_dim * 0.5,
            side_dim * 0.5,
        ).buffer(base_plate_radius)

        infill = honeycomb_a.get_honeycomb_structure_for_poly(
            shape.buffer(10),
            honeycomb_regions=100,
            honeycomb_scale=14,
            wall_offset=-4,
            region_min=2,
            region_max=6,
            seed=0,
        )

        shape = unary_union(
            [
                shape - shape.buffer(-5),
                shape - infill,
            ]
        )

        for i in range(4):
            a = math.pi * 0.5 * i

            tab = box(0, 0, self.tab_length, self.wood_thickness_tab_hole_size())
            tab_0 = translate(
                tab,
                self.tab_offset_from_center,
                self.side_length * 0.5 + self.bend_radius - self.wood_thickness,
            )
            tab_1 = translate(
                tab,
                -self.tab_offset_from_center - self.tab_length,
                self.side_length * 0.5 + self.bend_radius - self.wood_thickness,
            )

            tabs = unary_union([tab_0, tab_1])
            tabs = rotate(tabs, a, (0, 0), use_radians=True)

            tabs_outer = tabs.buffer(4)
            shape = unary_union([shape, tabs_outer]) - tabs

        m.add_poly(shape)

        return m

    def get_top_plate_model(self):
        m = Model()

        positive = []
        negative = []

        support_width = 10

        tab_dist_from_origin = (
            self.side_length * 0.5 + self.bend_radius - self.wood_thickness
        )

        for i in range(4):
            a = math.pi * 0.5 * i

            tab = box(0, 0, self.tab_length, self.wood_thickness_tab_hole_size())
            tab_0 = translate(
                tab,
                self.tab_offset_from_center,
                tab_dist_from_origin,
            )
            tab_1 = translate(
                tab,
                -self.tab_offset_from_center - self.tab_length,
                tab_dist_from_origin,
            )

            tabs = unary_union([tab_0, tab_1])
            tabs = rotate(tabs, a, (0, 0), use_radians=True)

            tabs_outer = tabs.convex_hull.buffer(4)
            positive.append(tabs_outer)
            negative.append(tabs)

        positive.append(
            box(
                -support_width * 0.5,
                -tab_dist_from_origin,
                support_width * 0.5,
                tab_dist_from_origin,
            )
        )
        positive.append(
            box(
                -tab_dist_from_origin,
                -support_width * 0.5,
                tab_dist_from_origin,
                support_width * 0.5,
            )
        )

        shape = unary_union(positive) - unary_union(negative)

        m.add_poly(shape)

        return m

    def get_top_roof_angle_support(self, top_slot=False):
        m = Model()

        roof_height = 40
        roof_width = 10 + self.side_length * 0.5 + self.bend_radius

        shape = Polygon(
            [
                [-roof_width, 0],
                [roof_width, 0],
                [0, roof_height],
            ]
        )

        cut = box(
            -self.wood_thickness_tab_hole_size() * 0.5,
            0,
            self.wood_thickness_tab_hole_size() * 0.5,
            roof_height * 0.5,
        )

        if top_slot:
            cut = translate(cut, yoff=roof_height * 0.5)

        shape = shape.difference(cut)

        m.add_poly(shape)

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        model.add_model(self.get_bendy_model()).renderer.translate(
            z=self.wood_thickness
        )

        model.add_model(self.get_base_plate_model()).renderer.color(0.75, 0.45, 0.0)

        model.add_model(self.get_top_plate_model()).renderer.color(
            0.75, 0.45, 0.0
        ).translate(z=self.bend_shape_height + self.wood_thickness)

        model.add_model(self.get_top_roof_angle_support()).renderer.rotate(
            a=90, v=[1, 0, 0]
        ).translate(
            y=self.wood_thickness * 0.5,
            z=self.bend_shape_height + self.wood_thickness + self.wood_thickness,
        ).color(
            0.75, 0.45, 0.0
        )

        model.add_model(self.get_top_roof_angle_support(top_slot=True)).renderer.rotate(
            a=90, v=[1, 0, 0]
        ).rotate(a=90, v=[0, 0, 1]).translate(
            x=-self.wood_thickness * 0.5,
            z=self.bend_shape_height + self.wood_thickness + self.wood_thickness,
        )

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
