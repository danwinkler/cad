import math
import random
import time
from collections import defaultdict

import mcubes
import numba
import numpy as np
from _cython_csg import CSG
from numba import float32, float64, guvectorize, njit, vectorize
from project.python_conv_surf import cuda_conv
from project.python_conv_surf import main as conv_main
from solid import *
from solid.utils import *
from stl import mesh

from lib.helper import *


class GridStore:
    def __init__(self):
        self.points = defaultdict(list)
        self.connections = []

    def put(self, a, b):
        self.points[a].append(b)
        self.points[b].append(a)
        self.connections.append(Line(a, b))


DEPTH = 10
WIDTH = 100
THICKNESS = 2
W2 = WIDTH / 2

holes = []
block = cube([WIDTH + THICKNESS, WIDTH + THICKNESS, 10])

grid = GridStore()

for i in range(4):
    # 90deg from center
    t = math.pi * 0.5

    angle = t * i

    center = Vec3(W2, W2, 0)
    out = center + Vec3(math.cos(angle) * W2, math.sin(angle) * W2, 0)
    right = out + Vec3(math.cos(angle + t) * W2, math.sin(angle + t) * W2, 0)
    left = out + Vec3(math.cos(angle - t) * W2, math.sin(angle - t) * W2, 0)

    mid_t = math.pi * 0.2
    mid_d = W2 * 0.3

    mid_a = (center + right + out) * (1.0 / 3.0)
    mid_b = (center + left + out) * (1.0 / 3.0)

    center.round()
    out.round()
    right.round()
    left.round()
    mid_a.round()
    mid_b.round()

    grid.put(center, out)
    grid.put(out, right)
    grid.put(right, center)
    grid.put(out, left)
    grid.put(center, mid_a)
    grid.put(out, mid_a)
    grid.put(right, mid_a)

    grid.put(center, mid_b)
    grid.put(out, mid_b)
    grid.put(left, mid_b)

margin = 10
height = 10

fminx = -10
fminy = -10
fminz = -10

fres = 0.5
field, fwidth, fheight, fdepth = conv_main.generate_field(
    fminx, fminy, fminz, 110, 110, height + margin, fres
)

s = 3.0

triangles = []
for line in grid.connections:
    triangles.append(
        [
            [line.a.x, line.a.y, 0],
            [line.b.x, line.b.y, 0],
            [line.b.x, line.b.y, height],
            [s, 0.0, 0.0],
        ]
    )

    triangles.append(
        [
            [line.a.x, line.a.y, 0],
            [line.b.x, line.b.y, height],
            [line.a.x, line.a.y, height],
            [s, 0.0, 0.0],
        ]
    )

triangles = np.array(triangles)

assert triangles.dtype == np.float64
assert field.dtype == np.float64

print(
    f"Starting field calulation, field size: {field.shape}, num objects: {len(triangles)}"
)
start = time.time()

field = cuda_conv.cuda_calculate_field(field, triangles)
end = time.time()
print(f"Finished field calc, took {end-start:2f} seconds")

grid3 = field.reshape(fwidth, fheight, fdepth)

print("Starting marching cubes")
vertices, triangles = mcubes.marching_cubes(grid3, 0.005)
print(f"Finished marching cubes, output model has {len(triangles)} triangles")

# vertices = [[float(i) for i in v] for v in vertices]
# triangles = [[int(i) for i in t] for t in triangles]

path = __file__ + ".conv.stl"

data = np.zeros(len(triangles), dtype=mesh.Mesh.dtype)
for i, point in enumerate(triangles):
    data["vectors"][i] = np.array([vertices[i] * fres for i in point])

m = mesh.Mesh(data)
m.save(path)

parts = []

sidemargin = 2
parts.append(
    translate([sidemargin, sidemargin, 0])(
        translate([fminx, fminy, fminz])(import_stl(path))
    )
    - translate([-10, -10, -10])(
        cube([200, 200, 200])
        - translate([10, 10, 10])(
            cube([WIDTH + sidemargin * 2, WIDTH + sidemargin * 2, DEPTH])
        )
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
