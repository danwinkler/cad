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


def box_joints(
    p0,
    p1,
    wood_thickness,
    alternate=False,
    offset=0,
    joint_width=10,
    kerf=0.11,
    kerf_start=False,
    kerf_end=False,
):
    """Generate a series of boxes along the vector between p0 and p1"""

    def calculate_angle(p0, p1):
        return math.atan2(p1.y - p0.y, p1.x - p0.x)

    def create_rectangle(center_x, center_y, width, height, angle):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        dx = width / 2
        dy = height / 2
        corners = [
            (
                center_x - dx * cos_angle + dy * sin_angle,
                center_y - dx * sin_angle - dy * cos_angle,
            ),
            (
                center_x + dx * cos_angle + dy * sin_angle,
                center_y + dx * sin_angle - dy * cos_angle,
            ),
            (
                center_x + dx * cos_angle - dy * sin_angle,
                center_y + dx * sin_angle + dy * cos_angle,
            ),
            (
                center_x - dx * cos_angle - dy * sin_angle,
                center_y - dx * sin_angle + dy * cos_angle,
            ),
        ]
        return Polygon(corners)

    angle = calculate_angle(p0, p1)
    length = math.hypot(p1.x - p0.x, p1.y - p0.y)
    num_joints = int(length // (joint_width)) + 2

    rectangles = []
    for i in range(num_joints):
        if alternate == (i % 2 == 1):
            continue

        t_offset = offset

        t_kerf = 0
        t_kerf_start = kerf_start or len(rectangles) > 0
        t_kerf_end = kerf_end or i < num_joints - 3
        if t_kerf_start:
            t_kerf += kerf
            t_offset += kerf / joint_width
        if t_kerf_end:
            t_kerf += kerf
            t_offset -= kerf / joint_width

        center_x = p0.x + (i + 0.5 + t_offset) * joint_width * math.cos(angle)
        center_y = p0.y + (i + 0.5 + t_offset) * joint_width * math.sin(angle)

        rect = create_rectangle(
            center_x, center_y, joint_width - t_kerf, wood_thickness * 2, angle
        )

        rectangles.append(rect)

    poly = MultiPolygon(rectangles)

    # Finally, chop off each end
    center = (p0 + p1) / 2
    allowed_area = create_rectangle(
        center.x, center.y, length, wood_thickness * 2, angle
    ).buffer(
        0.0001
    )  # For numerical stability
    poly = poly.intersection(allowed_area)

    return poly


def clean(poly: MultiPolygon):
    return poly
    okay_polys = []

    for p in poly.geoms:
        if p.area > 0.1:
            okay_polys.append(p)

    return MultiPolygon(okay_polys)


class Shelves:
    def __init__(
        self,
    ):
        self.wood_thickness = 5
        self.shelf_depth = 4.5 * in_to_mm
        self.top_shelf_height = 7 * in_to_mm
        self.joint_width = 10

        self.counter_depth = 24 * in_to_mm
        self.counter_width = 49.5 * in_to_mm

        self.total_width = 49 * in_to_mm

        self.l_depth = 22.5 * in_to_mm
        self.l_width = 10 * in_to_mm
        self.back_shelf_width = (self.total_width - self.l_width) / 2
        self.back_support_width = 30

        self.vertical_joint_size = (self.top_shelf_height + self.wood_thickness) / 14

        self.vertical_color = (0.8, 0.5, 0.2)

    def l_shape(self):
        shape = box(0, 0, self.l_width, self.l_depth)
        shape -= box(self.shelf_depth, 0, self.l_width, self.l_depth - self.shelf_depth)

        shape -= unary_union(
            [
                # Front
                box_joints(
                    p0=euclid3.Point2(0, 0),
                    p1=euclid3.Point2(self.shelf_depth, 0),
                    wood_thickness=self.wood_thickness,
                    alternate=True,
                    offset=-0.5,
                    joint_width=self.joint_width,
                ),
                # Back
                box_joints(
                    p0=euclid3.Point2(0, self.l_depth),
                    p1=euclid3.Point2(self.shelf_depth, self.l_depth),
                    wood_thickness=self.wood_thickness,
                    alternate=True,
                    offset=-0.5,
                    joint_width=self.joint_width,
                    kerf_end=True,
                ),
                # Left
                box_joints(
                    p0=euclid3.Point2(0, self.l_depth),
                    p1=euclid3.Point2(0, self.l_depth - self.shelf_depth),
                    wood_thickness=self.wood_thickness,
                    offset=-1.5,
                    joint_width=self.joint_width,
                    kerf_end=True,
                ),
                # Right
                box_joints(
                    p0=euclid3.Point2(self.l_width, self.l_depth),
                    p1=euclid3.Point2(self.l_width, self.l_depth - self.shelf_depth),
                    wood_thickness=self.wood_thickness,
                    offset=-1.5,
                    joint_width=self.joint_width,
                ),
            ]
        )

        return shape

    def l_bottom(self):
        shape = self.l_shape()

        m = Model()

        m.add_poly(shape)

        return m

    def l_top(self):
        shape = self.l_shape()

        m = Model()

        m.add_poly(shape).translate(z=self.top_shelf_height)

        return m

    def end_cap(self):
        shape = box(0, 0, self.shelf_depth, self.top_shelf_height + self.wood_thickness)

        shape -= unary_union(
            [
                box_joints(
                    p0=euclid3.Point2(0, 0),
                    p1=euclid3.Point2(self.shelf_depth),
                    wood_thickness=self.wood_thickness,
                    offset=-0.5,
                    joint_width=self.joint_width,
                ),
                box_joints(
                    p0=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
                    p1=euclid3.Point2(
                        self.shelf_depth, self.top_shelf_height + self.wood_thickness
                    ),
                    wood_thickness=self.wood_thickness,
                    offset=-0.5,
                    joint_width=self.joint_width,
                ),
            ]
        )

        return shape

    def l_front(self):
        shape = self.end_cap()

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).translate(
            y=self.wood_thickness
        ).color(*self.vertical_color)

        return m

    def l_back(self):
        shape = self.end_cap()

        shape -= box_joints(
            p0=euclid3.Point2(0, 0),
            p1=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
            wood_thickness=self.wood_thickness,
            offset=-0,
            joint_width=self.vertical_joint_size,
        )

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).translate(y=self.l_depth).color(
            *self.vertical_color
        )

        return m

    def l_left(self):
        shape = self.end_cap()

        shape -= box_joints(
            p0=euclid3.Point2(0, 0),
            p1=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
            wood_thickness=self.wood_thickness,
            offset=-1,
            joint_width=self.vertical_joint_size,
        )

        shape = clean(shape)

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).rotate(
            a=-90, v=(0, 0, 1)
        ).translate(x=self.wood_thickness, y=self.l_depth).color(0.7, 0.7, 0.2)

        return m

    def l_right(self):
        shape = self.end_cap()

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).rotate(
            a=-90, v=(0, 0, 1)
        ).translate(x=self.l_width, y=self.l_depth).color(0.7, 0.7, 0.2)

        return m

    def get_L_models(self):
        return [
            self.l_bottom(),
            self.l_top(),
            self.l_front(),
            self.l_back(),
            self.l_left(),
            self.l_right(),
        ]

    def back_shape(self):
        shape = box(0, 0, self.back_shelf_width, self.shelf_depth)

        shape -= unary_union(
            [
                # Left
                box_joints(
                    p0=euclid3.Point2(0, self.shelf_depth),
                    p1=euclid3.Point2(0, 0),
                    wood_thickness=self.wood_thickness,
                    offset=-1.5,
                    joint_width=self.joint_width,
                ),
                # Right
                box_joints(
                    p0=euclid3.Point2(self.back_shelf_width, self.shelf_depth),
                    p1=euclid3.Point2(self.back_shelf_width, 0),
                    wood_thickness=self.wood_thickness,
                    offset=-1.5,
                    joint_width=self.joint_width,
                ),
                # Back Left Support
                box_joints(
                    p0=euclid3.Point2(0, self.shelf_depth),
                    p1=euclid3.Point2(self.back_support_width, self.shelf_depth),
                    wood_thickness=self.wood_thickness,
                    offset=-1,
                    joint_width=self.joint_width,
                    kerf_end=True,
                ),
                # Back right support
                box_joints(
                    p0=euclid3.Point2(self.back_shelf_width, self.shelf_depth),
                    p1=euclid3.Point2(
                        self.back_shelf_width - self.back_support_width,
                        self.shelf_depth,
                    ),
                    wood_thickness=self.wood_thickness,
                    offset=-1,
                    joint_width=self.joint_width,
                    kerf_end=True,
                ),
            ]
        )

        return shape

    def back_bottom(self):
        shape = self.back_shape()

        m = Model()

        m.add_poly(shape)

        return m

    def back_top(self):
        shape = self.back_shape()

        m = Model()

        m.add_poly(shape).translate(z=self.top_shelf_height)

        return m

    def back_back_support(self):
        shape = box(
            0, 0, self.back_support_width, self.top_shelf_height + self.wood_thickness
        )

        shape -= unary_union(
            [
                box_joints(
                    p0=euclid3.Point2(0, 0),
                    p1=euclid3.Point2(self.back_support_width, 0),
                    wood_thickness=self.wood_thickness,
                    offset=-0,
                    joint_width=self.joint_width,
                ),
                box_joints(
                    p0=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
                    p1=euclid3.Point2(
                        self.back_support_width,
                        self.top_shelf_height + self.wood_thickness,
                    ),
                    wood_thickness=self.wood_thickness,
                    offset=-0,
                    joint_width=self.joint_width,
                ),
            ]
        )

        return shape

    def back_left(self):
        shape = self.end_cap()

        shape -= box_joints(
            p0=euclid3.Point2(0, 0),
            p1=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
            wood_thickness=self.wood_thickness,
            offset=-1,
            joint_width=self.vertical_joint_size,
        )

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).rotate(
            a=-90, v=(0, 0, 1)
        ).translate(x=self.wood_thickness, y=self.shelf_depth).color(
            *self.vertical_color
        )

        return m

    def back_back_left(self):
        shape = self.back_back_support()

        shape -= box_joints(
            p0=euclid3.Point2(0, 0),
            p1=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
            wood_thickness=self.wood_thickness,
            offset=-0,
            joint_width=self.vertical_joint_size,
        )

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).translate(
            x=0, y=self.shelf_depth
        ).color(0.7, 0.7, 0.2)

        return m

    def back_right(self):
        shape = self.end_cap()

        shape -= box_joints(
            p0=euclid3.Point2(0, 0),
            p1=euclid3.Point2(0, self.top_shelf_height + self.wood_thickness),
            wood_thickness=self.wood_thickness,
            offset=-1,
            joint_width=self.vertical_joint_size,
        )

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).rotate(
            a=-90, v=(0, 0, 1)
        ).translate(x=self.back_shelf_width, y=self.shelf_depth).color(0.7, 0.7, 0.2)

        return m

    def back_back_right(self):
        shape = self.back_back_support()

        shape -= box_joints(
            p0=euclid3.Point2(self.back_support_width, 0),
            p1=euclid3.Point2(
                self.back_support_width, self.top_shelf_height + self.wood_thickness
            ),
            wood_thickness=self.wood_thickness,
            offset=-0,
            joint_width=self.vertical_joint_size,
        )

        m = Model()

        m.add_poly(shape).rotate(a=90, v=(1, 0, 0)).translate(
            x=self.back_shelf_width - self.back_support_width, y=self.shelf_depth
        ).color(*self.vertical_color)

        return m

    def get_back_shelf(self):
        return [
            self.back_bottom(),
            self.back_top(),
            self.back_left(),
            self.back_back_left(),
            self.back_right(),
            self.back_back_right(),
        ]

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 580, 580)

        for m in self.get_L_models():
            model.add_model(m)

        spacing = 10

        back_shelf_locations = [
            euclid3.Point2(self.l_width + spacing, self.l_depth - self.shelf_depth),
            euclid3.Point2(
                self.l_width + self.back_shelf_width + 2 * spacing,
                self.l_depth - self.shelf_depth,
            ),
        ]

        for pos in back_shelf_locations:
            for m in self.get_back_shelf():
                model.add_model(m).renderer.translate(x=pos.x, y=pos.y)

        return model


m = Shelves()

# DEBUG
# debug_scalar = 0.5
# m.l_width *= debug_scalar
# m.l_depth *= debug_scalar
# m.top_shelf_height = m.vertical_joint_size * 3.5
# m.shelf_depth *= debug_scalar

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
