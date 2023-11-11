import math
import pathlib
import random
import subprocess
import tempfile
from dataclasses import dataclass

import cv2
import diskcache
import euclid3
import numpy as np
import pyclipper
import rtree
import shapelysmooth
import solid
from fontTools.ttLib import TTFont
from scipy.spatial import Voronoi
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.common.lasercut import Model, MultipartModel, s_poly_to_scad, skeleton_to_polys

# from cad.common.helper import *


# random.seed(0)

model = MultipartModel()

cache = diskcache.FanoutCache(
    tempfile.gettempdir() + "/" + pathlib.Path(__file__).stem + ".cache"
)


def get_outer_shape():
    """
    This is just a random shape for testing
    """
    steps = 10

    def skel_fn(i):
        a = (i / steps) * math.pi * 0.5
        return (math.cos(a) * 100, math.sin(a) * 100, 1000 - i * 15)

    outline_skeleton = [(skel_fn(i), skel_fn(i + 1)) for i in range(steps - 1)]

    outline_polys = skeleton_to_polys(
        outline_skeleton, im_scale=3.0, blur=201, margin=100, threshold=8
    )

    return unary_union(outline_polys)


@cache.memoize()
def get_honeycomb_structure_for_poly(
    poly,
    honeycomb_regions=100,
    honeycomb_scale=2,
    wall_offset=-0.3,
    region_min=10,
    region_max=30,
    seed=0,
):
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

    # Caculating Voronoi
    vor = Voronoi([(p.x, p.y) for p in points])

    # Remove incomplete regions
    regions = list(filter(lambda x: all(i >= 0 for i in x) and len(x) > 0, vor.regions))

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

    # Offset polygons
    holes = []
    for region in regions:
        verts = [vor.vertices[r] for r in region]
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(
            pyclipper.scale_to_clipper([[v[0], v[1]] for v in verts]),
            pyclipper.JT_MITER,
            pyclipper.ET_CLOSEDPOLYGON,
        )

        p2 = pyclipper.scale_from_clipper(
            pco.Execute(pyclipper.scale_to_clipper(wall_offset))
        )

        cutout = [Polygon(path) for path in p2]

        holes.append(cutout)

    return unary_union(holes)


if __name__ == "__main__":
    outer_poly = get_outer_shape()

    outer_poly = shapelysmooth.taubin_smooth(outer_poly, 0.2, 0.2, 5)

    honeycomb = get_honeycomb_structure_for_poly(
        outer_poly,
        honeycomb_regions=100,
        region_min=5,
        region_max=10,
        honeycomb_scale=12,
        wall_offset=-0.6,
    )

    outline_skeleton = []
    for i in range(len(outer_poly.exterior.coords)):
        a = outer_poly.exterior.coords[i]
        b = outer_poly.exterior.coords[(i + 1) % len(outer_poly.exterior.coords)]
        outline_skeleton += [((a[0], a[1], 1000), (b[0], b[1], 1000))]

    outline_polys = skeleton_to_polys(
        outline_skeleton, im_scale=8.0, blur=21, margin=50, threshold=8
    )

    outline_polys = [
        shapelysmooth.taubin_smooth(poly, 0.2, 0.2, 5) for poly in outline_polys
    ]

    final_poly = unary_union(outline_polys + [honeycomb]).intersection(outer_poly)

    # Remove any holes that are too small
    min_area = 1
    final_poly = Polygon(
        final_poly.exterior.coords,
        [i for i in final_poly.interiors if Polygon(i).area > min_area],
    )

    model.add_part(final_poly)

    # model.add_part(honeycomb)

    top_level_geom = model.render_scad()

    # model.render_single_svg(__file__ + ".svg")
    model.render_single_dxf(__file__ + ".dxf")

    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(solid.scad_render(top_level_geom))
