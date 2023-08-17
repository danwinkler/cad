import math
import random

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

    def distance(self, point):
        return self.pos.distance(point)

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

    def distance(self, point):
        return self.pos.distance(point)

    def __repr__(self):
        return self.pos.__repr__()


cloud = []
points = []
for i in range(12):
    a = (i / 12.0) * math.pi * 2
    points.append(Point(math.cos(a), math.sin(a), 0))

A = 0.01
B = -0.1
f_max = 0.5
f_min = -0.5


def force_function(distance):
    if distance == 0:
        return 0
    f = 1.0 / (distance**2)
    return f


def control_function(x, y, z):
    f = Vec3(x, y, z)
    a = 0
    for p in points:
        v = f - p.pos
        mag = v.length()
        a += force_function(mag)
    return a


for x in np.arange(-2, 2, 0.1):
    for y in np.arange(-2, 2, 0.1):
        for z in np.arange(-2, 2, 0.1):
            v = abs(control_function(x, y, z))
            if v > 15 and v < 16:
                cloud.append(Point(x, y, z))

vecs = [f.pos for f in cloud]
string_out = "\n".join([" ".join([str(v) for v in f.to_list()]) for f in vecs])
with open("torus.xyz", "w") as f:
    f.write(string_out)
