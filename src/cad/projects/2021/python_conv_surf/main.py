import math
import time
import random
from functools import reduce

import mcubes
from _cython_csg import CSG
import numba
import numpy as np
from stl import mesh
from numba import float32, float64, guvectorize, njit, vectorize
from scipy.spatial import Voronoi

from .cuda_conv import cuda_calculate_field

from . import voronoi3d


def generate_field(minx, miny, minz, maxx, maxy, maxz, resolution):
    # The following code generates a 2d array: (x*y*z, 3), where the last dimension is the xyz coord
    x = np.arange(minx, maxx, resolution)
    y = np.arange(miny, maxy, resolution)
    z = np.arange(minz, maxz, resolution)
    meshgrid = np.meshgrid(x, y, z)
    return np.vstack(meshgrid).reshape(3, -1).T, x.shape[0], y.shape[0], z.shape[0]

    # The following code generates a 4d array: (x, y, z, 3), where the last dimension is the xyz coord
    # meshgrid = np.meshgrid(
    #     np.arange(minx, maxx, resolution),
    #     np.arange(miny, maxy, resolution),
    #     np.arange(minz, maxz, resolution),
    #     indexing="ij",
    # )
    # return np.stack(meshgrid, axis=3)


# TODO: experiment with inlining all of these helpers
# https://numba.pydata.org/numba-doc/latest/developer/inlining.html

if __name__ == "__main__":
    field, width, height, depth = generate_field(-10, -10, -10, 110, 110, 110, 1.0)

    # triangles = []

    # fn = lambda x, y: math.sin(x) + math.cos(y)
    # s = 4
    # for x in np.arange(0, 10, 0.5):
    #     for y in np.arange(0, 10, 0.5):
    #         triangles += [
    #             [
    #                 [x, y, fn(x, y)],
    #                 [x + 1, y, fn(x + 1, y)],
    #                 [x + 1, y + 1, fn(x + 1, y + 1)],
    #                 [s, 0, 0],
    #             ],
    #             [
    #                 [x, y, fn(x, y)],
    #                 [x, y + 1, fn(x, y + 1)],
    #                 [x + 1, y + 1, fn(x + 1, y + 1)],
    #                 [s, 0, 0],
    #             ],
    #         ]

    triangles = []
    triangles += [
        [
            [5, 5, -3],
            [5, 5, 3],
            [math.nan, math.nan, math.nan],
            [2, 0, 0],
        ],
    ]

    # triangles += [
    #     [
    #         [-5, 5, -3],
    #         [-5, 5, 3],
    #         [math.nan, math.nan, math.nan],
    #         [2, 0, 0],
    #     ],
    # ]

    # Sphere with holes
    # sphere = CSG.sphere(radius=3.9, slices=24, stacks=12)
    # a = CSG.cylinder(start=[-4, 0, 0], end=[4, 0, 0], radius=2, slices=32)
    # b = CSG.cylinder(start=[0, -4, 0], end=[0, 4, 0], radius=2, slices=32)
    # c = CSG.cylinder(start=[0, 0, -4], end=[0, 0, 4], radius=2, slices=32)

    # polygons = (sphere - (a + b + c)).toPolygons()

    # Random cylinders
    # random.seed(0)
    # cylinders = [
    #     CSG.cylinder(
    #         start=[random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)],
    #         end=[random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)],
    #         radius=0.5,
    #         slices=8,
    #     )
    #     for i in range(10)
    # ]

    # polygons = reduce(lambda a, b: a + b, cylinders).toPolygons()

    # need to do if polygons is output from csg
    # polygons = [[[v.pos.x, v.pos.y, v.pos.z] for v in p.vertices] for p in polygons]

    # Load stl
    # stl_mesh = mesh.Mesh.from_file("project/honeycomb/mesh3d.stl")

    # polygons = stl_mesh.points.reshape(-1, 3, 3)

    # s = 10

    # triangles = []
    # for p in polygons:
    #     # Simple triangulation that assumes that polygon is convex (not sure if true)
    #     for i in range(len(p) - 2):
    #         triangles.append([p[0], p[i + 1], p[i + 2], [s, 0.0, 0.0]])

    # from . import voronoi3d

    # triangles = []
    # s = 2
    # for ridge in voronoi3d.ridge_list:
    #     triangles.append(
    #         [
    #             ridge.p0.p.to_list(),
    #             ridge.p1.p.to_list(),
    #             [math.nan, math.nan, math.nan],
    #             [s, 0.0, 0.0],
    #         ]
    #     )

    triangles = np.array(triangles)
    print(triangles)

    assert triangles.dtype == np.float64
    assert field.dtype == np.float64

    print(
        f"Starting field calulation, field size: {field.shape}, num objects: {len(triangles)}"
    )
    start = time.time()

    field = cuda_calculate_field(field, triangles)
    end = time.time()
    print(f"Finished field calc, took {end-start:2f} seconds")

    grid3 = field.reshape(width, height, depth)

    print("Starting marching cubes")
    vertices, triangles = mcubes.marching_cubes(
        field.reshape(width, height, depth), 0.005
    )
    print(f"Finished marching cubes, output model has {len(triangles)} triangles")

    mcubes.export_obj(vertices, triangles, "test.obj")
