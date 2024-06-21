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
    SolidModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)
from cad.common.project_step import ProjectSteps

in_to_mm = 25.4


class Panels:
    def __init__(
        self,
        width,
        height,
        bar_1_height,
        bar_2_height,
        panel_margin_x=3,
        panel_margin_y=3,
    ):
        self.width = width
        self.height = height
        self.bar_1_height = bar_1_height
        self.bar_2_height = bar_2_height
        self.panel_margin_x = panel_margin_x
        self.panel_margin_y = panel_margin_y

        self.bar_height = 1.5 * in_to_mm
        self.inner_strut_size = 8
        self._infill = None
        self.screw_rad = 1.6
        self.screw_support_rad = 14

    def get_infill(self):
        if self._infill is None:
            self._infill = honeycomb_a.get_honeycomb_structure_for_poly(
                box(0, 0, self.width, self.height).buffer(20),
                honeycomb_regions=600,
                honeycomb_scale=20,
                region_min=2,
                region_max=6,
                wall_offset=-(self.inner_strut_size / 2),
            )

        return self._infill

    def generate_panel(
        self, x_pos, y_pos, panel_width, panel_height, wave_bottom=False, wave_top=False
    ) -> Model:
        shape = box(0, 0, panel_width, panel_height)

        screw_holes = []

        n_screws = 3
        if wave_top:
            shape = unary_union(
                [
                    shape,
                    Polygon(
                        [(panel_width, 0), (0, 0), (0, panel_height)]
                        + [
                            (
                                x,
                                panel_height
                                + (self.bar_height / 2)
                                + math.sin(x * (math.pi * 2 * n_screws / panel_width))
                                * self.bar_height
                                / 2,
                            )
                            for x in np.linspace(0, panel_width, 100)
                        ]
                    ),
                ]
            )

            for i in range(n_screws):
                x = panel_width / n_screws * (i + 0.25)
                y = panel_height + (self.bar_height / 2)

                screw_holes.append(Point(x, y))
        else:
            for i in range(n_screws):
                x = panel_width / (n_screws + 1) * (i + 1)
                y = panel_height - self.bar_height / 2

                screw_holes.append(Point(x, y))

        if wave_bottom:
            shape -= Polygon(
                [(panel_width, 0), (0, 0)]
                + [
                    (
                        x,
                        (self.bar_height / 2)
                        + math.sin(x * (math.pi * 2 * n_screws / panel_width))
                        * self.bar_height
                        / 2,
                    )
                    for x in np.linspace(0, panel_width, 100)
                ]
            )

            for i in range(n_screws):
                x = panel_width / n_screws * (i + 0.75)
                y = self.bar_height / 2

                screw_holes.append(Point(x, y))
        else:
            for i in range(n_screws):
                x = panel_width / (n_screws + 1) * (i + 1)
                y = self.bar_height / 2

                screw_holes.append(Point(x, y))

        inner_shape = shape.buffer(-self.inner_strut_size)
        infill = translate(
            self.get_infill(),
            -(x_pos + self.inner_strut_size),
            -(y_pos + self.inner_strut_size),
        )

        rim = shape - inner_shape

        shape = unary_union([rim, inner_shape - infill])

        # Add screw support holes
        for hole in screw_holes:
            shape = unary_union([shape, hole.buffer(self.screw_support_rad)])

        # Remove any holes that are too small
        min_area = 10
        shape = Polygon(
            shape.exterior.coords,
            [i for i in shape.interiors if Polygon(i).area > min_area],
        )

        # Add screw holes
        for hole in screw_holes:
            shape -= hole.buffer(self.screw_rad)

        m = Model()

        m.add_poly(shape)

        return m

    def get_backing_model(self):
        m = SolidModel()

        m.add_solid(
            solid.translate([-10, -10, -10])(
                solid.cube([self.width + 20, self.height + 20, 10])
                - solid.translate([10, 10, -1])(
                    solid.cube([self.width, self.height, 12])
                )
            )
        )

        # Bottom Bar
        m.add_solid(
            solid.translate([0, 0, -10])(solid.cube([self.width, self.bar_height, 10]))
        )

        # Bar 1
        m.add_solid(
            solid.translate([0, self.bar_1_height, -10])(
                solid.cube([self.width, self.bar_height, 10])
            )
        )

        # Bar 2
        m.add_solid(
            solid.translate([0, self.bar_2_height, -10])(
                solid.cube([self.width, self.bar_height, 10])
            )
        )

        # Top Bar
        m.add_solid(
            solid.translate([0, self.height - self.bar_height, -10])(
                solid.cube([self.width, self.bar_height, 10])
            )
        )

        return m

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 295, 580)

        model.add_model(self.get_backing_model()).renderer.color(r=0.8, g=0.5, b=0.2)

        # Row 0
        model.add_model(
            self.generate_panel(
                x_pos=0,
                y_pos=0,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.bar_1_height,
                wave_top=True,
            )
        )
        model.add_model(
            self.generate_panel(
                x_pos=self.width / 2,
                y_pos=0,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.bar_1_height,
                wave_top=True,
            )
        ).renderer.translate(self.width / 2)

        # Row 1
        model.add_model(
            self.generate_panel(
                x_pos=0,
                y_pos=self.bar_1_height + self.panel_margin_y,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.bar_2_height
                - self.bar_1_height
                - self.panel_margin_y,
                wave_bottom=True,
                wave_top=True,
            )
        ).renderer.translate(x=0, y=self.bar_1_height + self.panel_margin_y)

        model.add_model(
            self.generate_panel(
                x_pos=self.width / 2,
                y_pos=self.bar_1_height + self.panel_margin_y,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.bar_2_height
                - self.bar_1_height
                - self.panel_margin_y,
                wave_bottom=True,
                wave_top=True,
            )
        ).renderer.translate(
            x=self.width / 2, y=self.bar_1_height + self.panel_margin_y
        )

        # Row 2
        model.add_model(
            self.generate_panel(
                x_pos=0,
                y_pos=self.bar_2_height + self.panel_margin_y,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.height - self.bar_2_height - self.panel_margin_y,
                wave_bottom=True,
            )
        ).renderer.translate(y=self.bar_2_height + self.panel_margin_y)

        model.add_model(
            self.generate_panel(
                x_pos=self.width / 2,
                y_pos=self.bar_2_height + self.panel_margin_y,
                panel_width=self.width / 2 - self.panel_margin_x,
                panel_height=self.height - self.bar_2_height - self.panel_margin_y,
                wave_bottom=True,
            )
        ).renderer.translate(
            x=self.width / 2, y=self.bar_2_height + self.panel_margin_y
        )

        return model


side_1 = Panels(
    width=20 * in_to_mm,
    height=40.75 * in_to_mm,
    bar_1_height=16.5 * in_to_mm,
    bar_2_height=(16.5 + 1.5 + 17) * in_to_mm,
)

side_2 = Panels(
    width=23.75 * in_to_mm,
    height=40.25 * in_to_mm,
    bar_1_height=16 * in_to_mm,
    bar_2_height=(16 + 1.5 + 17) * in_to_mm,
    panel_margin_x=20,
)

m = side_1

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
