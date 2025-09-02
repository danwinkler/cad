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
import svgpath2mpl
import ziafont
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.common.lasercut import Model, MultipartModel, s_poly_to_scad


def make_octagon_box(
    side_length=60,
    height=40,
    wood_thickness=4.9,
    tab_width=10,
    kerf_adjustment=0.11,
):
    # Helper to get octagon points
    def octagon_points(center, radius):
        return [
            (
                center[0] + radius * math.cos(math.radians(45 * i)),
                center[1] + radius * math.sin(math.radians(45 * i)),
            )
            for i in range(8)
        ]

    # Outer octagon for top/bottom
    radius = side_length / (2 * math.sin(math.pi / 8))
    center = (radius, radius)
    oct_pts = octagon_points(center, radius)
    oct_poly = Polygon(oct_pts)

    # Sides: 8 panels, each with box joints
    def make_side(i):
        angle = 45 * i
        # Panel width is the distance between adjacent octagon vertices
        p0, p1 = oct_pts[i], oct_pts[(i + 1) % 8]
        panel_length = math.dist(p0, p1)
        # Extend panel so joints overlap
        # Calculate the required tab depth for 45-degree overlap
        # The tab needs to reach past the adjacent panel, so use wood_thickness / sin(45)
        tab_depth = wood_thickness / math.sin(math.pi / 4)
        joint_extension = tab_depth
        extended_length = panel_length + 2 * joint_extension
        panel = box(0, 0, extended_length, height)

        # Add box joints to left/right sides
        def joint_cut(start, end, offset=False):
            cuts = []
            y = start
            tab_idx = 0
            while y < end:
                # For the lowest tab (first one), do not offset by kerf
                if tab_idx == 0:
                    cuts.append(
                        box(
                            -wood_thickness,
                            y,
                            tab_depth + wood_thickness,
                            y + tab_width,
                        )
                    )
                else:
                    cuts.append(
                        box(
                            -wood_thickness,
                            y + (kerf_adjustment if not offset else -kerf_adjustment),
                            tab_depth + wood_thickness,
                            y
                            + tab_width
                            - (kerf_adjustment if not offset else -kerf_adjustment),
                        )
                    )
                y += tab_width * 2
                tab_idx += 1
            shape = unary_union(cuts)
            if offset:
                shape = box(-wood_thickness, start, tab_depth, end).difference(shape)
            return shape

        # Left joints
        panel = panel.difference(joint_cut(0, height, offset=False))
        # Right joints
        panel = panel.difference(
            translate(
                joint_cut(0, height, offset=True), xoff=extended_length - tab_depth
            )
        )
        return panel, angle, p0, p1, joint_extension, extended_length, panel_length

    # Build MultipartModel
    m = MultipartModel(wood_thickness)
    # Bottom
    m.add_model(Model(thickness=wood_thickness)).add_poly(oct_poly)
    # Sides
    wall_colors = [
        (0.8, 0.7, 0.2),
        (0.7, 0.4, 0.1),
    ]
    for i in range(8):
        panel, angle, p0, p1, joint_extension, extended_length, panel_length = (
            make_side(i)
        )
        model = Model(thickness=wood_thickness)
        model.add_poly(panel)
        dx, dy = p0[0], p0[1]
        edge_angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        shift_x = dx - joint_extension * math.cos(math.radians(edge_angle))
        shift_y = dy - joint_extension * math.sin(math.radians(edge_angle))
        # Alternate color for each wall
        color = wall_colors[i % len(wall_colors)]
        model.renderer.rotate(90, [1, 0, 0]).rotate(edge_angle, [0, 0, 1]).translate(
            shift_x, shift_y, 0
        ).color(*color)
        m.add_model(model)
    # Top
    m.add_model(Model(thickness=wood_thickness)).add_poly(oct_poly).translate(
        z=height - wood_thickness
    )
    return m


# Example usage
if __name__ == "__main__":
    model = make_octagon_box(
        side_length=60, height=40, wood_thickness=4.9, tab_width=10
    )
    output_dir = pathlib.Path(__file__).parent / (
        pathlib.Path(__file__).stem + "_parts"
    )
    model.render_parts(output_dir)
    model.render_single_dxf(output_dir / "single.dxf")
    top_level_geom = model.render_scad()
    print(f"Total Cut Length: {model.get_total_cut_length()}")
    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(solid.scad_render(top_level_geom))
