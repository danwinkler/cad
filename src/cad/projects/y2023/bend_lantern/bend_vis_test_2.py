"""
This method chops up the shape into segments and aligns them along the path
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

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
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

for i in range(0, int(base_perimeter_length), 10):
    shape -= Point(i, 10).buffer(3)


def extrude_polygon(polygon, height):
    if isinstance(polygon, Polygon):
        polys = [polygon]
    elif isinstance(polygon, MultiPolygon):
        polys = polygon.geoms

    vf = [
        trimesh.creation.triangulate_polygon(p, triangle_args="qpa0.001") for p in polys
    ]

    v, f = trimesh.util.append_faces([i[0] for i in vf], [i[1] for i in vf])

    mesh = trimesh.creation.extrude_triangulation(v, f, height)

    return mesh


def wrap_shape_around_base(shape, base, thickness=5):
    segments = []
    current_dist = 0
    for i, p in enumerate(base.exterior.coords):
        if i == 0:
            continue

        a = base.exterior.coords[i - 1]
        b = p

        d = Point(a).distance(Point(b))

        window = box(current_dist, shape.bounds[1], current_dist + d, shape.bounds[3])
        window = window.intersection(shape)

        if window.is_empty:
            continue

        mesh = extrude_polygon(window, thickness)
        angle = math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / math.pi
        segments.append(
            solid.translate([a[0], a[1], 0])(
                solid.rotate(v=euclid3.Vector3(0, 0, 1), a=angle)(
                    solid.translate([-current_dist, 0, 0])(
                        solid.rotate(v=euclid3.Vector3(-1, 0, 0), a=90)(
                            solid.polyhedron(
                                points=mesh.vertices,
                                faces=mesh.faces,
                            )
                        )
                    )
                )
            )
        )

        current_dist += d

    return segments


parts = wrap_shape_around_base(shape, base)
top_level_geom = solid.union()(parts)


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
