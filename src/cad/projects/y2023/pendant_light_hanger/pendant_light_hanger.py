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
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

# from cad.common.helper import *
from cad.projects.y2023.pendant_light_hanger.common import (
    MultipartModel,
    s_poly_to_scad,
    skeleton_to_polys,
)

random.seed(0)

parts = []


tab_positions = [0, 40, 80, 120]
board_thickness = 5
tab_height = 10
tab_depth = 12
tab_overhang = 10


def arch(notch=False):
    lines = []

    def lineFunc(i):
        p = i / segments
        a = (i / segments) * math.pi * 0.5
        return (
            600 - math.cos(a) * 600,
            math.sin(a) * 600,
            10000 - (9000 * p),
        )

    segments = 32
    for i in range(segments):
        lines.append(
            (
                lineFunc(i),
                lineFunc(i + 1),
            )
        )

        if notch and i > segments - 3:
            break

    polys = skeleton_to_polys(lines, im_scale=3.0, blur=201, margin=100, threshold=8)

    polys = [shapelysmooth.taubin_smooth(poly, 0.1, 0.1, 5) for poly in polys]
    # polys = [shapelysmooth.catmull_rom_smooth(poly, 0.5) for poly in polys]

    # There should be one poly rn
    poly = polys[0]

    # Make it flat against the wall
    poly -= box(-50, -20, 0, 200)

    # If notch, cut out a slot for the wire
    if notch:
        poly -= box(-50, -20, 10, 200)

        # We also want to make an indent along the top, so we do the following:
        # 1. Get a new poly that is shifted down n_y_shift amount
        n_y_shift = 6
        poly_shifted = translate(poly, 0, -n_y_shift)

        # 2. Substract poly_shifted from poly
        edge_poly = poly - poly_shifted

        # 3. subtract edge_poly from poly
        poly -= edge_poly

    # Tabs
    if not notch:
        tabs = []
        for y in tab_positions:
            tabs += [
                box(
                    -tab_depth,
                    y,
                    0,
                    y + tab_height,
                ),
                box(
                    -tab_depth,
                    y - tab_overhang,
                    -board_thickness,  # TODO: add a margin here
                    y + tab_height,
                ),
            ]

        poly = unary_union([poly] + tabs)

    # Registration holes
    hole_radius = 5

    # Along line segments
    hole_indicies = [
        5,
        11,
        17,
        23,
        27,
    ]

    for i in hole_indicies:
        x, y, v = lineFunc(i)
        poly -= Point(x, y).buffer(hole_radius)

    # Finally, split the poly into n parts such that it will fit on the build plate.

    if notch:
        split_points = [None, 9, 21, None]
    else:
        split_points = [None, 12, 24, None]

    polys = []
    for i in range(len(split_points) - 1):
        start = split_points[i]
        end = split_points[i + 1]

        def get_cut(i, side):
            a = lineFunc(i)
            b = lineFunc(i + 1)
            av = euclid3.Vector2(*a[:2])
            bv = euclid3.Vector2(*b[:2])
            v = bv - av
            v.normalize()
            cross = euclid3.Vector2(-v.y, v.x)

            cut_a = av + cross * 1000
            cut_b = cut_a + v * 1000 * side
            cut_c = cut_b - cross * 2000
            cut_d = av - cross * 1000

            cut_poly = Polygon([cut_a, cut_b, cut_c, cut_d])

            return cut_poly

        def get_connector(i, side):
            a = lineFunc(i)
            b = lineFunc(i + 1)
            av = euclid3.Vector2(*a[:2])
            bv = euclid3.Vector2(*b[:2])
            v = bv - av
            v.normalize()
            cross = euclid3.Vector2(-v.y, v.x)

            line_size = 20
            cross_size = 4
            cross_strength = 1000
            pa = av + v * line_size
            pb = av - v * line_size

            lines = [
                # This part goes along the arch
                ((pa.x, pa.y, 1000), (pb.x, pb.y, 1000)),
                # These short lines go sideways to create a little bump that the pieces will fit into tightly
                (
                    (
                        pa.x + cross.x * cross_size,
                        pa.y + cross.y * cross_size,
                        cross_strength,
                    ),
                    (
                        pa.x - cross.x * cross_size,
                        pa.y - cross.y * cross_size,
                        cross_strength,
                    ),
                ),
                (
                    (
                        pb.x + cross.x * cross_size,
                        pb.y + cross.y * cross_size,
                        cross_strength,
                    ),
                    (
                        pb.x - cross.x * cross_size,
                        pb.y - cross.y * cross_size,
                        cross_strength,
                    ),
                ),
            ]
            con_poly = skeleton_to_polys(
                lines, im_scale=2, blur=21, margin=200, threshold=2, debug_image=False
            )[0]

            con_poly = shapelysmooth.taubin_smooth(con_poly, 0.2, 0.2, 5)

            return con_poly

        our_poly = poly
        if start is not None:
            our_poly = poly - get_cut(start, -1)
            our_poly = our_poly - get_connector(start, -1)

        if end is not None:
            our_poly = our_poly - get_cut(end, 1)
            our_poly = unary_union([our_poly, get_connector(end, 1)])

        polys.append(our_poly)

    return polys


def backplate(latch=True):
    buffer = 0.5
    x_center = 80

    line_size = 100
    lines = [((x_center - line_size, 0, 1000), (x_center + line_size, 0, 1000))]
    polys = skeleton_to_polys(lines, im_scale=1, blur=181, margin=200, threshold=5)
    polys = [shapelysmooth.taubin_smooth(poly, 0.2, 0.2, 5) for poly in polys]
    poly = polys[0]

    if latch:
        for y in tab_positions:
            poly -= box(
                y,
                -board_thickness * 2 - buffer,
                y + tab_overhang + tab_height + buffer * 2,
                board_thickness * 2 + buffer,
            )

        screw_hole_rad = 4
    else:
        poly -= box(tab_positions[0] - 20, -10, tab_positions[-1] + 20, 10)
        screw_hole_rad = 1.5

    x_offset = 70
    y_offset = 22
    for x in [x_center - x_offset, x_center + x_offset]:
        for y in [-y_offset, y_offset]:
            poly -= Point(x, y).buffer(screw_hole_rad)

    return poly


model = MultipartModel(default_thickness=board_thickness)

expanded = True
expand_amount = 10 if expanded else 1

# Main arch
for i in range(4):
    arch_parts = arch(notch=i in [1, 2])
    for j, arch_part in enumerate(arch_parts):
        model.add_part(
            polygon=arch_part,
            translate=[
                expand_amount * j if expanded else 0,
                i * model.default_thickness * expand_amount,
                expand_amount * j if expanded else 0,
            ],
            rotate=((1, 0, 0), 90),
            color=[0.7, 0.7 - ((i + j) % 2) * 0.1, 0],
        )

for i in range(3):
    model.add_part(
        polygon=backplate(latch=i == 0),
        translate=[
            -i * board_thickness * expand_amount - expand_amount,
            board_thickness,  # This is just to align the backplate with the arch after all of the rotations
            0,
        ],
        rotate=((0, 1, 0), -90),
        color=[0.7, 0.7 - (i % 2) * 0.1, 0],
    )


top_level_geom = model.render_full()

output_dir = pathlib.Path(__file__).stem + "_parts"
# model.render_parts(output_dir)
# model.render_svgs(output_dir)

model.render_single_svg(__file__ + ".svg")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
