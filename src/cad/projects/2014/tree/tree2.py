import math
import random

from solid import *
from solid.utils import *

parts = []

max_i = 16
end_i = 8


def progress(i):
    global max_i, end_i
    return 1 - (float(i) / (max_i - end_i))


def make_branches(i):
    global max_i, end_i
    branches = []
    n = 2
    for j in range(n):
        a2 = random.uniform(1, 2) * i
        a1 = j * 180 + 90 * random.uniform(-15, 15)
        branches.append(rotate(a1, [0, 0, 1])(rotate(a2, [-1, 0, 0])(tree(i - 1))))
    return union()(branches)


def tree(i):
    global end_i
    if i == end_i:
        return sphere(i)
    return union()(
        hull()(sphere(i), translate([0, 0, i * 5])(sphere(i - 1))),
        translate([0, 0, i * 5])(make_branches(i)),
    )


parts.append(
    difference()(
        tree(max_i), translate([0, 0, -100])(cube([200, 200, 200], center=True))
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
