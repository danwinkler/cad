import itertools
import math
import random
import subprocess

import numpy as np
import visual as vi

from cad.common.helper import *


class Point:
    def __init__(self, x, y, z):
        self.pos = Vec3()
        self.set(x, y, z)

    def set(self, x, y, z):
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z

    def render(self):
        self.sphere = vi.sphere(pos=self.pos.to_list(), radius=0.1)

    def distance2(self, point):
        return self.pos.distance2(point)

    def __repr__(self):
        return self.pos.__repr__()


class Line:
    def __init__(self, p0, p1):
        self.p0 = p0.copy()
        self.p1 = p1.copy()

    def render(self):
        self.curve = vi.curve()
        self.curve.append(pos=self.p0.to_list())
        self.curve.append(pos=self.p1.to_list())

    def distance2(self, point):
        return point_to_line_segment_2(point, self.p0, self.p1)

    def __repr__(self):
        return self.pos.__repr__()


def get_points(
    lines,
    min_bound=Vec3(-1, -1, -1),
    max_bound=Vec3(1, 1, 1),
    resolution=0.05,
    d=12,
    r=1,
):
    lines = [[l.p0.to_list(), l.p1.to_list()] for l in lines]
    lines = np.array(lines)

    points = []
    xr = np.arange(min_bound.x, max_bound.x, resolution)
    yr = np.arange(min_bound.y, max_bound.y, resolution)
    zr = np.arange(min_bound.z, max_bound.z, resolution)

    def distance(A, B, P):
        """segment line AB, point P, where each one is an array([x, y])"""
        if (
            np.arccos(
                np.dot((P - A) / np.linalg.norm(P - A), (B - A) / np.linalg.norm(B - A))
            )
            > np.pi / 2
        ):
            return np.linalg.norm(P - A)
        if (
            np.arccos(
                dot((P - B) / np.linalg.norm(P - B), (A - B) / np.linalg.norm(A - B))
            )
            > np.pi / 2
        ):
            return np.linalg.norm(P - B)
        return abs(np.dot(A - B, P[::-1]) + np.linalg.det([A, B])) / np.linalg.norm(
            A - B
        )

    # Create x, y, z array with force value
    print(distance(lines[0], lines[1], [xr, yr, zr]))
    # loop over array and if force value is in range, add to point list

    xv, yv, zv = np.meshgrid(x_range, y_range, z_range)

    i = 0

    def filter_func(x, y, z):
        p = Vec3(x, y, z)
        v = 0
        for o in objs:
            v += 1.0 / o.distance2(p)
        r_min = d - r * 0.5
        r_max = d + r * 0.5
        if v > r_min and v < r_max:
            return True
        return False

    f = np.vectorize(filter_func)
    f = f(xv, yv, zv)

    for x, y, z in itertools.product(xv, yv, zv):
        pass

    return points


def write_points(points, filename):
    vecs = [f.pos for f in points]
    string_out = "\n".join([" ".join([str(v) for v in f.to_list()]) for f in vecs])
    with open(filename, "w") as f:
        f.write(string_out)


INV_SQ = 0
BLOBBY = 1
METABALL = 2
SOFT_OBJECT = 3


def make_points_file(
    lines,
    filename,
    min_bound=Vec3(-1, -1, -1),
    max_bound=Vec3(1, 1, 1),
    resolution=0.05,
    d=12,
    r=1,
    field_function=INV_SQ,
    function_opts=[],
):
    with open("temp.txt", "w") as f:
        first_line = " ".join([str(a) for a in min_bound.to_list()]) + " "
        first_line += " ".join([str(a) for a in max_bound.to_list()]) + " "
        first_line += (
            str(resolution)
            + " "
            + str(d)
            + " "
            + str(r)
            + " "
            + str(field_function)
            + " "
            + " ".join([str(o) for o in function_opts])
        )

        f.write(first_line + "\n")
        f.write(
            "\n".join(
                [
                    " ".join([str(a) for a in l.p0.to_list()])
                    + " "
                    + " ".join([str(a) for a in l.p1.to_list()])
                    for l in lines
                ]
            )
        )
    subprocess.call(["java", "PointCloud", "temp.txt", filename])
