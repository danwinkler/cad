import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

cutout = []
assembly = []

material_thickness = 6.5  # TODO measure

width = 100.0
height = 100.0
min_depth = 15.0
border = material_thickness + 5

cut_depth = min_depth * 0.75

inner_width = width - border * 2.0
inner_height = height - border * 2.0

x_sections = 5
y_sections = 5


def blob(x, y):
    w2 = width * 0.5
    h2 = height * 0.5
    xs = (w2 - abs(x - w2)) / w2
    ys = (h2 - abs(y - h2)) / h2
    return 50.0 / (1 + 10 * math.e ** -(0.1 * (xs * ys * 50)))


def sin(x, y):
    w2 = width * 0.5
    h2 = height * 0.5
    xs = (w2 - abs(x - w2)) / w2
    ys = (h2 - abs(y - h2)) / h2
    return 50 * math.sin(xs * math.pi * 0.5) * math.sin(ys * math.pi * 0.5)


func = sin


offset = 0
for x in range(x_sections):
    p = [[0, 0]]

    x_dist = border + (x / float(x_sections - 1)) * inner_width

    inc = inner_height / (y_sections - 1)
    for cut_y in range(y_sections):
        y_mid = border + inc * cut_y
        p.append([y_mid - material_thickness * 0.5, 0])
        p.append([y_mid - material_thickness * 0.5, cut_depth])
        p.append([y_mid + material_thickness * 0.5, cut_depth])
        p.append([y_mid + material_thickness * 0.5, 0])

    p.append([height, 0])
    p.append([height, min_depth + func(x_dist, height)])
    for i in range(y_sections):
        y = border + inner_height - (i / float(y_sections - 1)) * inner_height
        p.append([y, min_depth + func(x_dist, y)])

    p.append([0, min_depth + func(x_dist, 0)])
    poly = polygon(p)

    cutout.append(translate([0, offset, 0])(poly))
    offset += max(p, key=lambda o: o[1])[1] + 5

offset = 0
for y in range(y_sections):
    p = [[0, 0]]

    y_dist = border + (y / float(y_sections - 1)) * inner_height

    p.append([width, 0])
    p.append([width, min_depth + func(width, y_dist)])
    for i in range(x_sections):
        x = border + inner_height - (i / float(y_sections - 1)) * inner_height
        x1 = x + material_thickness * 0.5
        x2 = x - material_thickness * 0.5
        p.append([x1, min_depth + func(x1, y_dist)])
        p.append([x1, cut_depth])
        p.append([x2, cut_depth])
        p.append([x2, min_depth + func(x2, y_dist)])

    p.append([0, min_depth + func(x_dist, 0)])
    poly = polygon(p)

    cutout.append(translate([height + 5, offset, 0])(poly))
    offset += max(p, key=lambda o: o[1])[1] + 5

print("Saving File")
with open(__file__ + "_cutout.scad", "w") as f:
    f.write(scad_render(union()(cutout)))

with open(__file__ + "_assembly.scad", "w") as f:
    f.write(scad_render(union()(assembly)))
