"""
This test takes a 2d shape, triangulates it, extrudes it into a polyhedron, and then bends it around a 90 degree curve.
"""

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
import triangle
import trimesh
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils
from tqdm import tqdm

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    BendyRenderer,
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)

# from cad.common.helper import *


# random.seed(0)

side_length = 50
corner_radius = 30
corner_length = math.pi * corner_radius / 2
base_perimeter_length = (side_length + corner_length) * 4

base = box(
    corner_radius,
    corner_radius,
    corner_radius + side_length,
    corner_radius + side_length,
).buffer(corner_radius)

shape = box(0, 0, base_perimeter_length, 20)


def build_diamonds(
    n_rows, diamond_height, diamond_width, diamond_y_spacing, diamond_x_spacing, start
):
    diamonds = []
    for i in range(n_rows):
        for j in range(-2, 3):
            y = start.y + j * (diamond_height + diamond_y_spacing)
            if i % 2 == 0:
                y += (diamond_height + diamond_y_spacing) / 2

            x = start.x + i * (diamond_width + diamond_x_spacing)

            diamond = Polygon(
                [
                    (x, y),
                    (x + diamond_width / 2, y + diamond_height / 2),
                    (x + diamond_width, y),
                    (x + diamond_width / 2, y - diamond_height / 2),
                ]
            )

            diamonds.append(diamond)

    return unary_union(diamonds)


for i in range(4):
    start = Point(corner_length + i * (corner_length + side_length), 10)
    diamond_height = 24
    diamond_width = 1.5
    diamond_y_spacing = 3
    diamond_x_spacing = 0.8
    n_rows = int(corner_length / (diamond_width + diamond_x_spacing)) + 1
    diamonds = build_diamonds(
        n_rows=n_rows,
        diamond_height=diamond_height,
        diamond_width=diamond_width,
        diamond_y_spacing=diamond_y_spacing,
        diamond_x_spacing=diamond_x_spacing,
        start=start,
    )

    shape = shape.difference(diamonds)

model = MultipartModel()

model.add_part(shape, renderer=BendyRenderer(base))

top_level_geom = model.render_scad()

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
