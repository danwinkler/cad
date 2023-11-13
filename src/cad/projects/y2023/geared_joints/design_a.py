"""
This is a test of stacking a network of voronoi centroids on top of voronoi regions.

It looks bad.
"""

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
from scipy.spatial import Voronoi
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.common import gear
from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    SolidModel,
    s_poly_to_scad,
    shapely_to_solid,
    skeleton_to_polys,
)

# from cad.common.helper import *


# random.seed(0)


class ModelGen:
    def __init__(self):
        self.wood_thickness = 4.9

        self.arm_width = 40
        self.arm_length = 100
        self.internal_wall_thickness = 5
        self.axle_radius = 4

        self.teeth_count = 23

        self.bar_width = 20

        self.bearing_radius = 11
        self.bearing_thickness = 7
        self.bearing_pressfit_offset = 0.25

        # This is the distance from the outer edge of the bearing to the point where the inner part of the bearing starts to move
        # relative to the outer part. There's probably a better name for this
        self.bearing_outer_to_inner_offset = 2

        self.mount_screw_offset = 15
        self.mount_margin = 3
        self.mount_screw_radius = 1.75
        self.mount_screw_head_radius = 2.95
        self.mount_screw_head_height = 3.2
        self.mount_screw_nut_rad = 3.15  # Flat to flat hexagon

    def get_gear(self):
        gear_shape, pitch_radius = gear.generate(
            teeth_count=self.teeth_count,
            tooth_width=4.0,
        )

        return gear_shape, pitch_radius

    def arm(self, alternate=False, layer=0):
        m = Model()

        arm = box(-self.arm_width / 2, 0, self.arm_width / 2, self.arm_length)

        gear_shape, pitch_radius = self.get_gear()

        if alternate:
            gear_shape = rotate(gear_shape, 180 / self.teeth_count, origin=(0, 0))

        shape = unary_union([arm, gear_shape])

        nut_shape = Polygon(
            [
                (
                    math.cos(math.radians(60 * i + 30)) * self.mount_screw_nut_rad,
                    math.sin(math.radians(60 * i + 30)) * self.mount_screw_nut_rad,
                )
                for i in range(6)
            ]
        )

        if layer == 0:
            # TODO: this might need to be different as its where the nut will be. It also might need to be nut shaped so the nut cant rotate
            shape -= translate(nut_shape, xoff=self.mount_screw_offset)
            shape -= translate(nut_shape, xoff=-self.mount_screw_offset)
            shape -= Point(0, 0).buffer(
                self.bearing_radius - self.bearing_outer_to_inner_offset
            )

            # Spacer
            shape = unary_union(
                [
                    shape,
                    Point(0, 0).buffer(self.axle_radius + 2)
                    - Point(0, 0).buffer(self.axle_radius),
                ]
            )

        if layer == 1:
            shape -= Point(0, 0).buffer(self.bearing_radius)
            shape -= Point(self.mount_screw_offset, 0).buffer(self.mount_screw_radius)
            shape -= Point(-self.mount_screw_offset, 0).buffer(self.mount_screw_radius)

        if layer == 2:
            shape -= self.get_bearing_mount_outline()

        # cutout = honeycomb_a.get_honeycomb_structure_for_poly(
        #     shape,
        #     honeycomb_scale=13,
        #     region_min=3,
        #     wall_offset=-self.internal_wall_thickness / 2,
        #     region_max=6,
        # )

        # shape = shape - cutout.intersection(shape.buffer(-self.internal_wall_thickness))

        m.add_poly(shape)

        return m

    def connector_bar(self):
        m = Model()

        gear_shape, pitch_radius = self.get_gear()

        rounded_rad = 3

        shape = box(
            -self.bar_width / 2 + rounded_rad,
            -self.bar_width / 2 + rounded_rad,
            pitch_radius * 2 + self.bar_width / 2 - rounded_rad,
            self.bar_width / 2 - rounded_rad,
        )

        shape = shape.buffer(rounded_rad)

        shape -= Point(0, 0).buffer(self.axle_radius)
        shape -= Point(pitch_radius * 2, 0).buffer(self.axle_radius)

        m.add_poly(shape)

        return m

    def get_bearing_mount_outline(self):
        outline = unary_union(
            [
                Point(-self.mount_screw_offset, 0).buffer(self.mount_screw_radius),
                Point(self.mount_screw_offset, 0).buffer(self.mount_screw_radius),
                Point(0, 0).buffer(self.bearing_radius),
            ]
        ).convex_hull.buffer(self.mount_margin)

        return outline

    def get_bearing_mount(self):
        m = SolidModel()

        outline = self.get_bearing_mount_outline()

        bearing_shape = Point(0, 0).buffer(self.bearing_radius)

        part = shapely_to_solid(outline)

        part = solid.linear_extrude(self.wood_thickness)(part)

        part -= solid.translate([0, 0, -1])(
            solid.linear_extrude(self.bearing_thickness - self.wood_thickness + 1)(
                shapely_to_solid(bearing_shape)
            )
        )

        part -= solid.translate([0, 0, -1])(
            solid.cylinder(
                r=self.bearing_radius - self.bearing_outer_to_inner_offset,
                h=self.wood_thickness + 2,
                segments=32,
            )
        )

        screw_shape = solid.union()(
            solid.cylinder(
                r=self.mount_screw_radius,
                h=self.wood_thickness + 2,
                segments=16,
            ),
            solid.translate([0, 0, 2 + 1])(
                solid.cylinder(
                    r=self.mount_screw_head_radius,
                    h=self.wood_thickness,
                    segments=16,
                )
            ),
        )

        # Screw holes
        part -= solid.translate([self.mount_screw_offset, 0, -1])(screw_shape)
        part -= solid.translate([-self.mount_screw_offset, 0, -1])(screw_shape)

        m.add_solid(part)

        # Spacer
        spacer_outline = Point(0, 0).buffer(self.axle_radius + 2) - Point(0, 0).buffer(
            self.axle_radius + 0.25
        )

        spacer = shapely_to_solid(spacer_outline)

        spacer = solid.linear_extrude(
            self.wood_thickness - (self.bearing_thickness - self.wood_thickness)
        )(spacer)

        spacer = solid.translate(
            [0, 0, (self.bearing_thickness - self.wood_thickness)]
        )(spacer)

        m.add_solid(spacer)

        return m

    def get_multi_model(self):
        def get_color():
            return (
                0.5 + random.random() * 0.3,
                0.5 + random.random() * 0.3,
                0.3 + random.random() * 0.1,
            )

        model = MultipartModel(default_thickness=self.wood_thickness)

        explode_factor = 5

        gear_shape, pitch_radius = self.get_gear()

        angle = 45
        x_pos = math.cos(math.radians(angle)) * pitch_radius * 2
        y_pos = math.sin(math.radians(angle)) * pitch_radius * 2
        rot_angle = angle * 2

        n_layers = 3
        for i in range(n_layers):
            model.add_model(self.arm(layer=i)).renderer.rotate(90, [0, 0, 1]).translate(
                z=self.wood_thickness * i * explode_factor
            ).color(*get_color())

            model.add_model(self.arm(alternate=True, layer=i)).renderer.rotate(
                -90 + rot_angle, [0, 0, 1]
            ).translate(x_pos, y_pos, z=self.wood_thickness * i * explode_factor).color(
                *get_color()
            )

        model.add_model(self.connector_bar()).renderer.rotate(
            angle, [0, 0, 1]
        ).translate(z=self.wood_thickness * n_layers * explode_factor).color(
            *get_color()
        )

        model.add_model(self.connector_bar()).renderer.rotate(
            angle, [0, 0, 1]
        ).translate(z=-self.wood_thickness * explode_factor).color(*get_color())

        model.add_model(self.get_bearing_mount()).renderer.rotate(
            90, [0, 0, 1]
        ).translate(z=self.wood_thickness * (n_layers - 1) * explode_factor)

        model.add_model(self.get_bearing_mount()).renderer.rotate(
            rot_angle + 90, [0, 0, 1]
        ).translate(
            x=x_pos, y=y_pos, z=self.wood_thickness * (n_layers - 1) * explode_factor
        )

        model.add_model(self.get_bearing_mount()).renderer.rotate(
            a=180, v=[1, 0, 0]
        ).translate(-100, -100)

        return model


part = ModelGen()

model = part.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
model.render_parts(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
