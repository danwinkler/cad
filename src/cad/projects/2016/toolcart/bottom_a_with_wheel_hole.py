import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wall_thickness = 4

inner_x = 19
inner_y = 38

length = 60

outer_x = inner_x + wall_thickness * 2
outer_y = inner_y + wall_thickness * 2

offset = 0.15

parts = []

parts.append(cube([length, outer_x, outer_y]))
parts.append(cube([outer_x, length, outer_y]))
parts.append(up(outer_y - wall_thickness)(cube([outer_x, outer_y, 40])))

parts.append(
    hole()(
        translate([wall_thickness, wall_thickness, wall_thickness])(
            cube([inner_x, length, 100]),
            cube([length, inner_x, 100]),
        ),
        translate([wall_thickness, wall_thickness, outer_y + 10])(cube([50, 50, 50])),
    )
)

parts += [
    # Bottom going up
    translate([outer_x / 2.0, outer_y * 0.5, 0])(
        rotate(a=180, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([outer_x / 2.0, outer_y * 0.75, 0])(
        rotate(a=180, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # Side on y axis
    translate([0, outer_x * 0.5, outer_y * 0.33])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([0, outer_x * 0.5, outer_y * 0.66])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # Y Axis side hold points
    translate([0, length * 0.75, outer_y * 0.33])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([0, length * 0.75, outer_y * 0.66])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # Y Axis top side hold points
    translate([0, outer_y * 0.625, outer_y * 1.33])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([0, outer_x * 0.5, outer_y * 1.33])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # X Axis side hold points
    translate([length * 0.5, 0, outer_y * 0.5])(
        rotate(a=90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([length * 0.75, 0, outer_y * 0.5])(
        rotate(a=90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # X Axis reverse side hold point
    translate([length * 0.6, outer_x, outer_y * 0.5])(
        rotate(a=-90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([length * 0.8, outer_x, outer_y * 0.5])(
        rotate(a=-90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # Y Axis reverse side hold point
    translate([outer_x, length * 0.65, outer_y * 0.5])(
        rotate(a=90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([outer_x, length * 0.85, outer_y * 0.5])(
        rotate(a=90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    # Wheel hole
    translate([outer_x / 2.0, length * 0.8, -1])(
        hole()(cylinder(r=3, h=wall_thickness + 2, segments=12))
    ),
]


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

with open(__file__ + ".flipped.scad", "w") as f:
    f.write(scad_render(scale([-1, 1, 1])(union()(parts))))
