import math
import random

from solid import *
from solid.utils import *

parts = []

max_i = 20
end_i = 10


def progress(i):
    global max_i, end_i
    return 1 - (float(i) / (max_i - end_i))


def make_branches(i):
    global max_i, end_i
    n = random.uniform(i, max_i)
    if n > max_i - 1:
        n = 3
    elif n > max_i - (max_i / 7.0):
        n = 2
    elif n > max_i - (max_i / 5.0):
        n = 1
    else:
        n = 0
    branches = []
    for j in range(n):
        a2 = random.uniform(0, 30) * (progress(i) - 0.5)
        a1 = random.uniform(
            progress(i) * 180 * (1 - (a2 / 30)),
            360 - 180 * progress(i) * (1 - (a2 / 30)),
        )
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
