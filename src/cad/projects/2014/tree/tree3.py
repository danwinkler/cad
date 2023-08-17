import math
import random

from solid import *
from solid.utils import *

parts = []

max_i = 10
end_i = 2

random.seed(10)


def progress(i):
    return 1 - (float(i - end_i) / (max_i - end_i))


def delta(i):
    return math.sin(progress(i) * math.pi)


def norm(vec):
    mag = math.sqrt(sum([n**2 for n in vec]))
    return [a / mag for a in vec]


def add_vec(a, b):
    return [x + y for x, y in zip(a, b)]


def scale_vec(vec, scale):
    return [x * scale for x in vec]


def xy_func(i):
    return random.uniform(-progress(i), progress(i)) * 2


def tree(vec, i):
    global end_i
    if i == end_i:
        return sphere(1)

    norm_vec = norm(vec)
    delta_vec = norm([xy_func(i), xy_func(i), (1 - delta(i))])

    if i == max_i:
        delta_vec = [0, 0, 0]
    my_vec = scale_vec(norm(add_vec(norm_vec, scale_vec(delta_vec, 1))), i * 4)
    part = hull()(sphere(i, segments=10), translate(my_vec)(sphere(i - 1, segments=10)))

    n = random.randint(1, 2)

    branches = []
    for j in range(n):
        branches.append(tree(my_vec, i - 1))

    return union()(translate(my_vec)(branches), part)


parts.append(tree([0, 0, 1], max_i))

parts.append(translate([0, 0, -5])(cylinder(r=20, h=10, center=True)))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
