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
    FontRenderer,
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
        self.kerf = 0.1

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 550, 250)

        stack_height = 8
        diameter_part_count = 30
        radius = 50
        z_step = model.default_thickness * 3
        hole_width = 7

        mid_section_size = 10
        small_section_size = 6

        def get_pos(i, rad_offset=0):
            angle = i * 360 / diameter_part_count
            angle_rad = math.radians(angle)
            x = math.cos(angle_rad) * (radius + rad_offset)
            y = math.sin(angle_rad) * (radius + rad_offset)
            return [x, y]

        def get_hole(i, rot_offset=0, rad_offset=0):
            angle = i * 360 / diameter_part_count
            angle_rad = math.radians(angle)
            x = math.cos(angle_rad) * (radius + rad_offset)
            y = math.sin(angle_rad) * (radius + rad_offset)

            hole_shape = box(
                -model.default_thickness / 2 + self.kerf,
                -hole_width / 2 + self.kerf,
                model.default_thickness / 2 - self.kerf,
                hole_width / 2 - self.kerf,
            )

            return translate(
                rotate(hole_shape, angle=(i + rot_offset) * 360 / diameter_part_count),
                x,
                y,
            )

        def is_vert_support_a(i, z):
            """Triple split"""
            return i % small_section_size == z % small_section_size and z % 2 == 0

        def is_vert_support_b(i, z):
            """Single Diagonal"""
            if z >= stack_height - 1:
                return False
            return (i - 2) % small_section_size == z % small_section_size and z % 2 == 1

        def is_hori_support_a(i, z):
            return z % 2 == 0 and i % (mid_section_size) == 0

        def is_hori_support_b(i, z):
            return z % 2 == 1 and i % small_section_size == z % small_section_size

        def is_vert_support_c(i, z):
            """Bottom row only"""
            return z == 2 and is_vert_support_a(i, z - 2)

        def get_tangent_offset(delta_angle):
            """Calculates the additional length needed for a line at an angle delta_angle to intersect the tangent of a circle at the endpoint of a radius."""
            return radius * (1 - math.cos(delta_angle)) / math.cos(delta_angle)

        for z in range(1, stack_height):
            for i in range(diameter_part_count):
                holes = []
                if is_hori_support_a(i, z):
                    for j in range(0, mid_section_size, 2):
                        rot_offset = 0
                        rad_offset = 0
                        if is_vert_support_b(i + j - 1, z - 1):
                            rot_offset = -1
                            delta_angle = math.pi * 2 / diameter_part_count
                            rad_offset = get_tangent_offset(delta_angle)
                        holes.append(
                            get_hole(
                                (i + j) % diameter_part_count,
                                rot_offset=rot_offset,
                                rad_offset=rad_offset,
                            )
                        )
                elif is_hori_support_b(i, z):
                    for j in range(0, small_section_size, 2):
                        rot_offset = 0
                        rad_offset = 0
                        if is_vert_support_a(i + j - 1, z - 1):
                            rot_offset = -1
                            delta_angle = math.pi * 2 / diameter_part_count
                            rad_offset = get_tangent_offset(delta_angle)
                        elif is_vert_support_a(i + j + 1, z - 1):
                            rot_offset = 1
                            delta_angle = math.pi * 2 / diameter_part_count
                            rad_offset = get_tangent_offset(delta_angle)

                        holes.append(
                            get_hole(
                                (i + j) % diameter_part_count,
                                rot_offset=rot_offset,
                                rad_offset=rad_offset,
                            )
                        )

                if holes:
                    m = Model()

                    holes_shape = unary_union(holes)

                    shape = (
                        unary_union(
                            [
                                holes_shape,
                                LineString([h.centroid for h in holes]).buffer(0.5),
                            ]
                        )
                        .buffer(5)
                        .buffer(-2)
                    )

                    m.add_poly(shape - holes_shape)

                    svgfont = FontRenderer(
                        pathlib.Path(__file__).parent
                        / "../../../common/Roboto-Regular.ttf"
                    )

                    text_poly = svgfont.render(f"{i}, {z}", 0.2)

                    # Shift down
                    text_poly = translate(text_poly, xoff=-2)

                    # Rotate
                    text_poly = rotate(
                        text_poly, angle=(i + 1) * 360 / diameter_part_count + 90
                    )

                    a = holes[0].centroid
                    b = holes[1].centroid

                    center = ((a.x + b.x) / 2, (a.y + b.y) / 2)

                    # Move to piece
                    text_poly = translate(text_poly, center[0], center[1])

                    m.add_poly(text_poly, layer="text").color(0.8, 0.1, 0.1).translate(
                        z=0.1
                    )

                    model.add_model(m).renderer.translate(z=z * z_step)

                def make_vert(points, rot_offset=0):
                    m = Model()

                    connection_points = [
                        (
                            p
                            if p[2] == "bottom"
                            else (p[0], p[1] + model.default_thickness, p[2])
                        )
                        for p in points
                    ]

                    connector_lines = []
                    for cp_i, p in enumerate(connection_points):
                        if cp_i == 0:
                            continue

                        mid_way_point = (
                            (p[0] + points[cp_i][0]) / 2,
                            (p[1] + points[cp_i][1]) / 2,
                        )

                        connector_lines.append(
                            LineString((connection_points[0][:2], p[:2], mid_way_point))
                        )

                    connectors = unary_union(connector_lines).buffer(4).buffer(-2)

                    connectors -= unary_union(
                        [
                            box(
                                p[0] - hole_width / 2 - 3,
                                p[1],
                                p[0] + hole_width / 2 + 3,
                                p[1] + model.default_thickness,
                            )
                            for p in points
                        ]
                    )

                    shape = unary_union(
                        [
                            box(
                                p[0] - hole_width / 2 - self.kerf,
                                p[1],
                                p[0] + hole_width / 2 + self.kerf,
                                p[1] + model.default_thickness,
                            )
                            for p in points
                        ]
                        + [connectors]
                    )

                    m.add_poly(shape)

                    angle = (i + rot_offset) * 360 / diameter_part_count
                    angle_rad = math.radians(angle)

                    model.add_model(m).renderer.translate(
                        z=-model.default_thickness / 2
                    ).rotate(a=90, v=(1, 0, 0)).rotate(
                        a=angle + 90, v=(0, 0, 1)
                    ).translate(
                        x=a[0], y=a[1], z=z * z_step
                    ).color(
                        r=0.7, g=0.7, b=0.3
                    )

                if is_vert_support_a(i, z):
                    # Vertical
                    a = get_pos(i)
                    b = get_pos(
                        (i + 1) % diameter_part_count,
                        rad_offset=get_tangent_offset(
                            math.pi * 2 / diameter_part_count
                        ),
                    )

                    ab_dist = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

                    y_dist = z_step

                    points = [
                        # Start hole
                        (0, 0, "top"),
                        # Right up
                        (ab_dist, y_dist, "bottom"),
                        # Left up
                        (-ab_dist, y_dist, "bottom"),
                    ]

                    # Straight up
                    if z + 1 < stack_height - 1:
                        points.append((0, z_step * 2, "bottom"))

                    make_vert(points)
                elif is_vert_support_b(i, z):
                    # Vertical
                    a = get_pos(i)
                    b = get_pos(
                        (i + 1) % diameter_part_count,
                        rad_offset=get_tangent_offset(
                            math.pi * 2 / diameter_part_count
                        ),
                    )

                    ab_dist = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

                    y_dist = z_step

                    points = [
                        # Bottom Left
                        (0, 0, "top"),
                        # Top
                        (ab_dist, y_dist, "bottom"),
                    ]

                    make_vert(points)
                elif is_vert_support_c(i, z):
                    # Vertical
                    a = get_pos(i)
                    b = get_pos(
                        (i + 1) % diameter_part_count,
                        rad_offset=get_tangent_offset(
                            math.pi * 2 / diameter_part_count
                        ),
                    )

                    ab_dist = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

                    y_dist = z_step

                    points = [
                        # Start hole
                        (0, 0, "bottom"),
                        # Right down
                        (ab_dist, -y_dist, "top"),
                        # Left down
                        (-ab_dist, -y_dist, "top"),
                    ]

                    make_vert(points)

        return model


m = Diffuser()

model = m.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf", use_physics_packer=True)
model.render_parts(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
