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


class Shelf:
    def __init__(self):
        # Global settings
        self.wood_thickness = 5
        self.shelf_support_height = 100
        self.inner_segment_width = (
            3  # When using a sparse infill, this is the width of the infill segments
        )
        self.shelf_depth = 200
        self.shelf_width = 500
        self.wall_piece_count = 5
        self.wall_piece_margin = 50

        # Wall piece settings
        self.wall_piece_width = 30
        self.wall_piece_tab_length = 10
        self.wall_piece_tab_count = 5
        self.wall_piece_tab_margin = 10
        self.wall_piece_above_shelf_extent = 20
        self.wall_piece_screw_hole_margin = 20

        # Shelf settings
        self.shelf_to_support_tab_length = 10
        self.shelf_to_support_tab_count = 3
        self.shelf_to_support_tab_margin = 20

        # Support settings
        self.support_front_offset = 40

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def wall_piece_x_pos(self, idx):
        usable_space = self.shelf_width - 2 * self.wall_piece_margin
        return self.wall_piece_margin + idx * (usable_space) / (
            self.wall_piece_count - 1
        )

    def wall_to_support_tabs(self, i):
        usable_length = self.shelf_support_height - 2 * self.wall_piece_tab_margin
        return self.wall_piece_tab_margin + i * (
            usable_length - self.wall_piece_tab_length
        ) / (self.wall_piece_tab_count - 1)

    def wall_to_shelf_tabs(self):
        n_tabs = 3
        tab_width = 10
        tab_spacing = 10
        total_tab_width = n_tabs * tab_width + (n_tabs - 1) * tab_spacing
        tabs = []
        # Tabs are centered on 0
        for i in range(n_tabs):
            x = -total_tab_width / 2 + i * (tab_width + tab_spacing)
            tabs.append([x, x + tab_width])

        return tabs

    def shelf_to_support_tabs(self):
        usable_space = (
            self.shelf_depth
            - 2 * self.shelf_to_support_tab_margin
            - self.support_front_offset
        )
        tabs = []

        for i in range(self.shelf_to_support_tab_count):
            y = (
                self.shelf_to_support_tab_margin
                + self.support_front_offset
                + i
                * (usable_space - self.shelf_to_support_tab_length)
                / (self.shelf_to_support_tab_count - 1)
            )

            tabs.append([y, y + self.shelf_to_support_tab_length])

        return tabs

    def wall_piece_model(self, seed=0):
        m = Model()

        # These lists allow us to mandate areas that must be filled or left empty, without having to worry to much about ordering of
        # features. Note that negative features take precedence over positive features.
        negative = []
        positive = []

        support_exterior = box(
            0,
            0,
            self.wall_piece_width,
            self.shelf_support_height + self.wall_piece_above_shelf_extent,
        )
        support_interior = support_exterior.buffer(-self.inner_segment_width)

        infill = honeycomb_a.get_honeycomb_structure_for_poly(
            support_exterior,
            honeycomb_scale=7.5,
            wall_offset=-self.inner_segment_width / 2,
            seed=seed,
            region_min=2,
            region_max=8,
        )
        # support = unary_union([support, support_interior - infill])

        # Filter out any infill polygons that don't intersect support
        infill = unary_union(
            [
                i.buffer(self.inner_segment_width) - i
                for i in infill.geoms
                if i.intersects(support_exterior)
            ]
        )

        support = infill

        # Wall tabs
        tab_x_min = self.wall_piece_width / 2 - self.wood_thickness_tab_hole_size() / 2
        tab_x_max = self.wall_piece_width / 2 + self.wood_thickness_tab_hole_size() / 2
        for i in range(self.wall_piece_tab_count):
            y = self.wall_to_support_tabs(i)

            tab = box(
                tab_x_min,
                y,
                tab_x_max,
                y + self.wall_piece_tab_length,
            )

            negative.append(tab)
            positive.append(tab.buffer(self.inner_segment_width))

        # Shelf tabs
        tabs_locations = self.wall_to_shelf_tabs()
        for x_min, x_max in tabs_locations:
            tab = box(
                self.wall_piece_width / 2 + x_min,
                self.shelf_support_height,
                self.wall_piece_width / 2 + x_max,
                self.shelf_support_height + self.wood_thickness,
            )

            negative.append(tab)
            positive.append(tab.buffer(self.inner_segment_width))

        # Screw holes
        n_screws = 2
        screw_rad = 2
        screw_usable_space = (
            self.shelf_support_height - 2 * self.wall_piece_screw_hole_margin
        )
        for i in range(n_screws):
            for side in [-1, 1]:
                x = self.wall_piece_width / 2 + side * (self.wall_piece_width / 2)
                y = self.wall_piece_screw_hole_margin + screw_usable_space / (
                    n_screws - 1
                ) * (i)
                hole = Point(x, y).buffer(screw_rad)

                negative.append(hole)
                positive.append(hole.buffer(self.inner_segment_width))

        support = unary_union(positive + [support])
        support -= unary_union(negative)

        support = translate(support, -self.wall_piece_width / 2, 0)

        m.add_poly(support)

        return m

    def shelf_model(self):
        m = Model()

        # These lists allow us to mandate areas that must be filled or left empty, without having to worry to much about ordering of
        # features. Note that negative features take precedence over positive features.
        negative = []
        positive = []

        shelf = box(0, -self.shelf_depth, self.shelf_width, 0)

        infill = honeycomb_a.get_honeycomb_structure_for_poly(
            shelf.buffer(20),
            honeycomb_regions=800,
            honeycomb_scale=7.5,
            wall_offset=-self.inner_segment_width / 2,
            region_min=2,
            region_max=6,
            seed=11,
        )

        tab_section = box(0, -self.wood_thickness, self.shelf_width, 0)

        shelf_minus_tabs = shelf - tab_section

        shelf = unary_union(
            [
                shelf_minus_tabs - shelf_minus_tabs.buffer(-self.inner_segment_width),
                shelf_minus_tabs - infill,
            ]
        )

        for i in range(self.wall_piece_count):
            x_pos = self.wall_piece_x_pos(i)

            tabs_locations = self.wall_to_shelf_tabs()

            tabs = unary_union(
                [
                    box(
                        x_min,
                        -self.wood_thickness,
                        x_max,
                        0,
                    )
                    for x_min, x_max in tabs_locations
                ]
            )

            tabs = translate(tabs, x_pos, 0)

            positive += [tabs]

            support_tabs = self.shelf_to_support_tabs()

            for y_min, y_max in support_tabs:
                tab = box(
                    x_pos - self.wood_thickness_tab_hole_size() / 2,
                    -self.shelf_depth + y_min,
                    x_pos + self.wood_thickness_tab_hole_size() / 2,
                    -self.shelf_depth + y_max,
                )

                negative.append(tab)
                positive.append(tab.buffer(self.inner_segment_width))

        shelf = unary_union(positive + [shelf])
        shelf -= unary_union(negative)

        m.add_poly(shelf)

        return m

    def get_support_model(self, seed):
        m = Model()

        # These lists allow us to mandate areas that must be filled or left empty, without having to worry to much about ordering of
        # features. Note that negative features take precedence over positive features.
        negative = []
        positive = []

        bottom_offset = 5

        outline = box(
            bottom_offset,
            self.support_front_offset,
            self.shelf_support_height,
            self.shelf_depth,
        )

        wall_tab_section = box(
            0,
            self.shelf_depth - self.wood_thickness,
            self.shelf_support_height,
            self.shelf_depth,
        )

        outline -= wall_tab_section

        outline -= scale(
            Point(0, 0).buffer(1), self.shelf_support_height - 10, self.shelf_depth - 10
        )

        rounded_radius = 20
        outline -= translate(
            box(0, 0, rounded_radius, rounded_radius)
            - Point(0, 0).buffer(rounded_radius),
            self.shelf_support_height,
            self.support_front_offset,
        )

        infill = honeycomb_a.get_honeycomb_structure_for_poly(
            outline.buffer(10),
            honeycomb_regions=100,
            honeycomb_scale=14,
            wall_offset=-self.inner_segment_width / 2,
            region_min=2,
            region_max=6,
            seed=seed,
        )

        infill = unary_union(
            [
                i.buffer(self.inner_segment_width) - i
                for i in infill.geoms
                if i.intersects(outline)
            ]
        )

        support = infill

        # Backside
        support -= box(
            -100,
            self.shelf_depth - self.wood_thickness,
            self.shelf_support_height + 100,
            self.shelf_depth + 50,
        )
        support -= wall_tab_section

        # Topside
        support -= box(
            self.shelf_support_height,
            -50,
            self.shelf_support_height + 50,
            self.shelf_depth + 100,
        )

        support = unary_union(
            [
                support,
                # Back support
                support.convex_hull.intersection(
                    box(
                        -50,
                        self.shelf_depth
                        - self.wood_thickness
                        - self.inner_segment_width,
                        self.shelf_support_height,
                        self.shelf_depth - self.wood_thickness,
                    )
                ),
                # Top support
                support.convex_hull.intersection(
                    box(
                        self.shelf_support_height - self.inner_segment_width,
                        -50,
                        self.shelf_support_height,
                        self.shelf_depth - self.wood_thickness,
                    )
                ),
            ]
        )

        # Tabs connecting to wall piece
        for i in range(self.wall_piece_tab_count):
            y = self.wall_to_support_tabs(i)

            tab = box(
                y,
                self.shelf_depth - self.wood_thickness,
                y + self.wall_piece_tab_length,
                self.shelf_depth,
            )

            positive.append(tab)

        # Tabs connecting to shelf
        support_tabs = self.shelf_to_support_tabs()

        for y_min, y_max in support_tabs:
            tab = box(
                self.shelf_support_height,
                y_min,
                self.shelf_support_height + self.wood_thickness,
                y_max,
            )

            positive.append(tab)

        support = unary_union(positive + [support])
        support -= unary_union(negative)

        m.add_poly(support)

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        # These are hand picked for ones that look nice lol
        support_seeds = [0, 2, 3, 5, 7]

        for i in range(self.wall_piece_count):
            x_pos = self.wall_piece_x_pos(i)
            wall_piece = self.wall_piece_model(seed=i)
            wall_piece.rotate = (
                (1, 0, 0),
                90,
            )
            wall_piece.translate = (x_pos, 0, 0)

            model.add_model(wall_piece)

            support = self.get_support_model(seed=support_seeds[i])
            support.rotate = ((0, 1, 0), -90)
            support.translate = (x_pos + self.wood_thickness / 2, -self.shelf_depth, 0)
            support.color = (0.75, 0.45, 0.0)

            model.add_model(support)

        shelf = self.shelf_model()
        shelf.translate = (0, 0, self.shelf_support_height)
        shelf.color = (0.7, 0.5, 0.0)
        model.add_model(shelf)

        return model


shelf = Shelf()

# Override A
shelf.shelf_width = 300
shelf.wall_piece_count = 2

model = shelf.get_multi_model()

top_level_geom = model.render_full()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
model.render_dxfs(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
