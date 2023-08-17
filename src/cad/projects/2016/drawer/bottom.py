import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wood_thickness = 5.5
wall_thickness = 3

height = 12
length = 20

bod_size = wall_thickness * 2 + wood_thickness
lengthplusbody = length + bod_size

parts = [
    # outer walls
    cube([wall_thickness, lengthplusbody, height + wall_thickness]),
    cube([lengthplusbody, wall_thickness, height + wall_thickness]),
    # inner walls
    translate([wall_thickness + wood_thickness, wall_thickness + wood_thickness, 0])(
        cube([wall_thickness, wall_thickness + length, height + wall_thickness]),
        cube([wall_thickness + length, wall_thickness, height + wall_thickness]),
    ),
    # bridges
    up(height)(
        translate([0, wall_thickness + wood_thickness, 0])(
            cube(
                [
                    wall_thickness * 2 + wood_thickness,
                    wall_thickness + length,
                    wall_thickness,
                ]
            )
        ),
        translate([wall_thickness + wood_thickness, 0, 0])(
            cube(
                [
                    wall_thickness + length,
                    wall_thickness * 2 + wood_thickness,
                    wall_thickness,
                ]
            )
        ),
    ),
    # floor
    translate([bod_size, bod_size, 0])(cube([length, length, wall_thickness])),
    # screwholes
    translate([bod_size + length * 0.5, 0, height * 0.5])(
        rotate(a=90, v=[1, 0, 0])(screwhole("#8 Wood", bod_size + 1))
    ),
    translate([0, bod_size + length * 0.5, height * 0.5])(
        rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", bod_size + 1))
    ),
    translate([bod_size + length * 0.5, bod_size + length * 0.5, wall_thickness + 5])(
        screwhole("#8 Wood", wall_thickness + 6)
    ),
]


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
