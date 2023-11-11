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

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import Model, MultipartModel, s_poly_to_scad, skeleton_to_polys

# from cad.common.helper import *


# random.seed(0)


class ModelGen:
    def __init__(self):
        self.wood_thickness = 4.9
        self.points = None

    def get_points(
        self,
        poly,
        honeycomb_scale=2,
        honeycomb_regions=100,
        region_min=2,
        region_max=5,
        seed=0,
    ):
        if self.points:
            return self.points

        random.seed(seed)

        expanded_poly = poly.buffer(honeycomb_scale * 2)

        min_dist = 0.8 * honeycomb_scale
        min_dist2 = min_dist * min_dist

        poly_min_x = poly.bounds[0]
        poly_min_y = poly.bounds[1]
        poly_max_x = poly.bounds[2]
        poly_max_y = poly.bounds[3]

        points = []
        index = rtree.index.Index()

        print("Building initial point set")
        for i in range(honeycomb_regions):
            print(str(i) + " out of " + str(honeycomb_regions))

            tx = random.uniform(poly_min_x, poly_max_x)
            ty = random.uniform(poly_min_y, poly_max_y)

            if not expanded_poly.contains(Point(tx, ty)):
                continue

            axis = euclid3.Vector3(0, 0, 1)
            angle = math.pi * random.uniform(0, 2)

            w = random.randint(region_min, region_max)
            h = random.randint(region_min, region_max)

            for y in range(h):
                for x in range(w):
                    offset = 0 if y % 2 == 0 else 0.5
                    # offset -= 5
                    p = euclid3.Vector3(x + offset, y * math.sin(math.pi / 3), 0)
                    p *= honeycomb_scale
                    p = p.rotate_around(axis, angle)
                    p.x += tx
                    p.y += ty

                    if not expanded_poly.contains(Point(p.x, p.y)):
                        continue

                    # points = list(
                    #     filter(lambda tp: (tp - p).magnitude_squared() > min_dist2, points)
                    # )
                    # points.append(p)

                    # Get points within min_dist
                    nearest = list(index.nearest((p.x, p.y, p.x, p.y), 1))

                    if len(nearest) > 0:
                        nearest = nearest[0]
                        tp = points[nearest]
                        if (tp - p).magnitude_squared() < min_dist2:
                            continue

                    points.append(p)
                    index.insert(len(points) - 1, (p.x, p.y, p.x, p.y))

        self.points = points
        return points

    def get_layer(self, connectors=False):
        m = Model()

        shape = box(0, 0, 100, 100)

        honeycomb_scale = 10
        points = self.get_points(
            shape, honeycomb_scale=honeycomb_scale, honeycomb_regions=100
        )

        # Caculating Voronoi
        vor = Voronoi([(p.x, p.y) for p in points])

        # Remove incomplete regions
        regions = list(
            filter(lambda x: all(i >= 0 for i in x) and len(x) > 0, vor.regions)
        )

        def area(corners):
            return Polygon(corners).area

        # Remove too big regions
        regions = list(
            filter(
                lambda region: area([vor.vertices[r] for r in region])
                < 10 * honeycomb_scale * honeycomb_scale,
                regions,
            )
        )

        line_buffer = 0.8
        if connectors:
            lines = []
            for a, b in vor.ridge_points:
                pa = points[a]
                pb = points[b]
                lines.append(
                    LineString([(pa.x, pa.y), (pb.x, pb.y)]).buffer(line_buffer)
                )

            shape = unary_union(lines).intersection(shape)
        else:
            holes = []
            for region in regions:
                if len(region) == 0:
                    continue

                corners = [vor.vertices[r] for r in region]

                poly = Polygon(corners)

                if not poly.is_valid:
                    continue

                holes.append(poly.buffer(-line_buffer))

            shape = shape.difference(unary_union(holes))

        m.add_poly(shape)

        return m

    def get_multi_model(self):
        model = MultipartModel(default_thickness=self.wood_thickness)

        model.add_model(self.get_layer())
        model.add_model(self.get_layer(True)).renderer.translate(
            0, 0, self.wood_thickness
        )

        return model


part = ModelGen()

model = part.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
# model.render_dxfs(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
