import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

inner_width = 148
inner_length = 68
inner_height = 22

wall_thickness = 5
back_wall = 11

outer_x = inner_width + wall_thickness * 2
outer_y = inner_length + wall_thickness + back_wall
outer_z = inner_height * 0.5 + wall_thickness


def rounded_edges(w, l, h, r):
    return translate([r, r, r])(
        minkowski()(cube([w - r * 2, l - r * 2, h - r * 2]), sphere(r=r, segments=32))
    )


def flat_top_round(w, l, h, r):
    return rounded_edges(w, l, h + r, r) - up(h)(cube([w, l, r]))


def hinge_cutout():
    return translate([-10, -1, -8])(
        cube([20, 2, 9]),
        up(3.1)(
            right(3.75)(rotate(a=90, v=[1, 0, 0])(cylinder(r=1, h=9))),
            right(20 - 3.75)(rotate(a=90, v=[1, 0, 0])(cylinder(r=1, h=9))),
        ),
    )


bottom = flat_top_round(outer_x, outer_y, outer_z, wall_thickness)
bottom -= translate([wall_thickness, wall_thickness, wall_thickness])(
    cube([inner_width, inner_length, inner_height * 0.5 + 1])
)
bottom -= translate([outer_x * 0.25, outer_y, outer_z])(hinge_cutout())

bottom -= translate([outer_x * 0.75, outer_y, outer_z])(hinge_cutout())

top = bottom.copy()

support_height = 2.5

support_locs = [[15, 15], [10, 55], [133, 15], [138, 55]]

for a in support_locs:
    top += translate([a[0] + wall_thickness, a[1] + wall_thickness, wall_thickness])(
        cylinder(r=2, h=support_height, segments=16)
    )

print("Saving File")
with open(__file__[:-3] + "_bottom.scad", "w") as f:
    f.write(scad_render(union()(bottom)))

with open(__file__[:-3] + "_top.scad", "w") as f:
    f.write(scad_render(union()(top)))
