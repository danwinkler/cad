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

shape = box(0, 0, 100, 100)
shape -= Point(50, 50).buffer(20)


def get_triangulation_input(polygon):
    pts = []
    seg = []
    holes = []

    if isinstance(polygon, Polygon):
        polys = [polygon]
    elif isinstance(polygon, MultiPolygon):
        polys = polygon.geoms

    for poly in polys:
        offset = len(pts)
        for i, p in enumerate(poly.exterior.coords):
            pts.append(p)
            seg.append([offset + i, offset + (i + 1) % len(poly.exterior.coords)])

        for interior in poly.interiors:
            offset = len(pts)
            for i, p in enumerate(interior.coords):
                pts.append(p)
                seg.append([offset + i, offset + (i + 1) % len(interior.coords)])

            # Find point within interior and add it to holes
            p = interior.centroid
            interior_polygon = Polygon(interior)
            for i in range(500):
                if interior_polygon.contains(p):
                    holes.append([p.x, p.y])
                    break
                p = Point(
                    interior.bounds[0] + random.random() * interior.bounds[2],
                    interior.bounds[1] + random.random() * interior.bounds[3],
                )
            else:
                raise Exception("Couldn't find point within interior")

    return {
        "vertices": pts,
        "segments": seg,
        "holes": holes,
    }


# tri = get_triangulation_input(shape)

# t = triangle.triangulate(tri, "p")

# scad_tris = []
# for triangle in t["triangles"]:
#     a, b, c = triangle
#     p0 = tri["vertices"][a]
#     p1 = tri["vertices"][b]
#     p2 = tri["vertices"][c]
#     scad_tris.append(
#         solid.linear_extrude(random.random())(
#             solid.polygon(
#                 points=[p0, p1, p2],
#                 paths=[[0, 1, 2]],
#             )
#         )
#     )

# top_level_geom = solid.union()(scad_tris)


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


mesh = extrude_polygon(shape, 10)

v, f = trimesh.remesh.subdivide_to_size(mesh.vertices, mesh.faces, max_edge=10)
mesh = trimesh.Trimesh(vertices=v, faces=f)


def bend_points(points):
    def mutate(p):
        x, y, z = p
        theta = x / 100 * math.pi / 2
        depth = z
        return (
            math.cos(theta) * (100 + z),
            math.sin(theta) * (100 + z),
            y,
        )

    return [mutate(p) for p in points]


points = bend_points(mesh.vertices)

top_level_geom = solid.polyhedron(points=points, faces=mesh.faces)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
