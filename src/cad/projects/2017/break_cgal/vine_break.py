import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

point_count = 10
distance = math.pi * 0.5
points = [
    Vec3(math.cos(a) * 10, math.sin(a) * 10, 0)
    for a in [(i / float(point_count - 1)) * distance for i in range(point_count)]
]

v = vine(points, lambda h, a: 1, sections=12)


def half():
    return translate([-2, 0, 0])(vine(points, lambda h, a: 1, sections=12)) - translate(
        [-5, 0, -5]
    )(cube([5, 20, 10]))


def arch():
    return half() + translate([0.001, 0, 0])(mirror([1, 0, 0])(half()))


parts.append(arch())

parts.append(translate([-5, -5, 0])(arch()))

parts.append(translate([5, -5, 0])(arch()))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
