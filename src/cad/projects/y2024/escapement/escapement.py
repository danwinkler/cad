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
    FontRenderer,
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

        self.internal_wall_thickness = 5

        self.teeth_count = 20

        self.bar_width = 20

        self.gear_base_radius = 40

        self.bearing_radius = 11
        self.bearing_thickness = 7
        self.bearing_pressfit_offset = 0.11

        # This is the distance from the outer edge of the bearing to the point where the inner part of the bearing starts to move
        # relative to the outer part. There's probably a better name for this
        self.bearing_outer_to_inner_offset = 2

        self.mount_screw_offset = 15
        self.mount_margin = 3
        self.mount_screw_radius = 1.75
        self.mount_screw_head_radius = 2.95
        self.mount_screw_head_height = 3.2
        self.mount_screw_nut_rad = 3.15  # Flat to flat hexagon

    def create_escapement_gear_shape(self, base_radius, tooth_length, a, b, num_teeth):
        """
        Creates a Shapely polygon for a gear used in an anchor escapement.

        Parameters:
        - base_radius (float): The radius of the base circle of the gear.
        - tooth_length (float): The length of the teeth.
        - a (float): The entry angle of the tooth (in degrees).
        - b (float): The exit angle of the tooth (in degrees).
        - num_teeth (int): The number of teeth on the gear.

        Returns:
        - Polygon: A Shapely polygon representing the gear.
        """

        def polar_to_cartesian(r, theta):
            """Convert polar coordinates to Cartesian coordinates."""
            return r * math.cos(theta), r * math.sin(theta)

        # Convert angles to radians
        a_rad = math.radians(a)
        b_rad = math.radians(b)

        # Angle between each tooth center
        tooth_angle = 2 * math.pi / num_teeth

        # Generate points for the gear
        points = []
        for i in range(num_teeth):
            # Center angle for this tooth
            center_angle = i * tooth_angle

            # Points for the base of the tooth
            base_left = polar_to_cartesian(base_radius, center_angle - b_rad / 2)
            base_right = polar_to_cartesian(base_radius, center_angle + a_rad / 2)

            # Point for the tip of the tooth (ensuring it's a sharp point)
            tip = polar_to_cartesian(base_radius + tooth_length, center_angle)

            # Add the points for this tooth
            points.extend([base_left, tip, base_right])

        # Create and return the gear polygon
        return Polygon(points)

    def escapement_gear(self):
        m = Model()

        # gear_shape, pitch_radius = self.get_gear()

        gear_shape = self.create_escapement_gear_shape(
            base_radius=self.gear_base_radius,
            tooth_length=10,
            a=25,
            b=-5,
            num_teeth=self.teeth_count,
        )

        gear_internal_structure = Point(0, 0).buffer(self.gear_base_radius - 5)

        internal_strut_count = 10
        for i in range(internal_strut_count):
            angle = i * (math.pi * 2 / internal_strut_count)
            a = Point(
                math.cos(angle) * self.gear_base_radius,
                math.sin(angle) * self.gear_base_radius,
            )

            gear_internal_structure = gear_internal_structure - LineString(
                [Point(0, 0), a]
            ).buffer(2)

        gear_internal_structure -= Point(0, 0).buffer(self.bearing_radius + 4)
        gear_internal_structure = unary_union(
            [
                gear_internal_structure,
                Point(0, 0).buffer(self.bearing_radius - self.bearing_pressfit_offset),
            ]
        )

        gear_shape = gear_shape.difference(gear_internal_structure)

        m.add_poly(gear_shape)

        return m

    def anchor(self):
        right_angle = math.pi / 2 - math.radians(45)
        left_angle = math.pi / 2 + math.radians(50)
        right_hook_tip_depth = 8
        right_hook_tip_angle_offset = math.radians(3)
        left_hook_tip_depth = 8
        gear_center_y = self.gear_base_radius + 30
        shape = Polygon(
            [
                # Topmost point
                (0, 5),
                # Rightmost point
                (
                    math.cos(right_angle) * (self.gear_base_radius + 25),
                    math.sin(right_angle) * (self.gear_base_radius + 25)
                    - gear_center_y,
                ),
                # Right hook tip
                (
                    math.cos(right_angle + right_hook_tip_angle_offset)
                    * (self.gear_base_radius + right_hook_tip_depth),
                    math.sin(right_angle + right_hook_tip_angle_offset)
                    * (self.gear_base_radius + right_hook_tip_depth)
                    - gear_center_y,
                ),
                # Right hook return
                (
                    math.cos(right_angle + math.radians(5))
                    * (self.gear_base_radius + 20),
                    math.sin(right_angle + math.radians(5))
                    * (self.gear_base_radius + 20)
                    - gear_center_y,
                ),
                # Top bottom
                (0, -5),
                # Left hook return
                (
                    math.cos(left_angle - math.radians(5))
                    * (self.gear_base_radius + 20),
                    math.sin(left_angle - math.radians(5))
                    * (self.gear_base_radius + 20)
                    - gear_center_y,
                ),
                # Left hook tip
                (
                    math.cos(left_angle)
                    * (self.gear_base_radius + left_hook_tip_depth),
                    math.sin(left_angle) * (self.gear_base_radius + left_hook_tip_depth)
                    - gear_center_y,
                ),
                # Leftmost point
                (
                    math.cos(left_angle) * (self.gear_base_radius + 25),
                    math.sin(left_angle) * (self.gear_base_radius + 25) - gear_center_y,
                ),
            ]
        )

        shape = shape.buffer(1)

        shape = unary_union(
            [
                shape,
                Point(0, 0).buffer(self.bearing_radius + 3),
            ]
        )
        shape -= Point(0, 0).buffer(self.bearing_radius - self.bearing_pressfit_offset)

        m = Model()

        m.add_poly(shape)

        return m

    def test_baseplate(self):
        m = Model()

        baseplate = LineString([(0, 0), (0, self.gear_base_radius + 30)]).buffer(20)

        baseplate -= Point(0, 0).buffer(self.mount_screw_radius)
        baseplate -= Point(0, self.gear_base_radius + 30).buffer(
            self.mount_screw_radius
        )

        m.add_poly(baseplate)

        return m

    def bearing_pressfit_test(self):
        radii = [self.bearing_radius + i for i in np.linspace(-0.2, 0.2, 5)]

        m = Model()

        fr = FontRenderer(
            pathlib.Path(__file__).parent / "../../../common/Roboto-Regular.ttf"
        )

        base = LineString(
            [
                (0, 0),
                (0, (max(radii) + 2) * 2 * len(radii)),
            ]
        ).buffer(max(radii) + 5)

        for i, r in enumerate(radii):
            center_y = i * 2 * (max(radii) + 2)
            base -= Point(0, center_y).buffer(r)

            text_poly = scale(
                fr.render(str(r), font_scale=10),
                xfact=0.03,
                yfact=0.03,
                origin=(0, 0),
            )

            text_poly = translate(text_poly, xoff=8, yoff=center_y + 8)

            m.add_poly(text_poly, layer="text").color(0.8, 0.1, 0.1).translate(z=0.1)

        m.add_poly(base)

        return m

    def get_multi_model(self):
        def get_color():
            return (
                0.5 + random.random() * 0.3,
                0.5 + random.random() * 0.3,
                0.3 + random.random() * 0.1,
            )

        model = MultipartModel(default_thickness=self.wood_thickness)

        model.add_model(self.escapement_gear())

        rot = -5

        model.add_model(self.anchor()).renderer.rotate(a=rot, v=[0, 0, 1]).translate(
            y=self.gear_base_radius + 30
        )

        model.add_model(self.test_baseplate()).renderer.translate(
            z=-self.wood_thickness
        ).color(*get_color())

        model.add_model(self.bearing_pressfit_test()).renderer.translate(x=100)

        return model


part = ModelGen()

model = part.get_multi_model()

top_level_geom = model.render_scad()

# output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
# model.render_parts(output_dir)

model.render_single_dxf(__file__ + ".dxf")

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
