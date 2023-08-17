import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wall_thickness = 4

inner_x = 19
inner_y = 38

length = 40
side_length = 40

outer_x = inner_x + wall_thickness * 2
outer_y = inner_y + wall_thickness * 2

wood_lip_extra = 6
angle_offset = 20 - 2
angle = -36.87

parts = []

side_wall_base = cube([outer_x + side_length, outer_y, wall_thickness])

front_wall = up(wall_thickness)(cube([wall_thickness, outer_y, length]))

side_wall = translate([outer_x - wall_thickness, 0, wall_thickness])(
    cube([side_length + wall_thickness, outer_y, wood_lip_extra])
)

floor = up(wall_thickness)(cube([outer_x + side_length, wall_thickness, length]))

cut = hole()(
    translate([wall_thickness + inner_x + angle_offset, wall_thickness, 0])(
        rotate(a=angle, v=[0, 0, 1])(translate([0, -10, 0])(cube([50, 60, 50])))
    )
)

holes = hole()(
    translate([0, wall_thickness + inner_x * 0.5, wall_thickness + length * 0.5])(
        rotate(v=[0, 1, 0], a=-90)(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate([outer_x * 0.5, 0, outer_y * 0.5 - 5])(
        rotate(v=[1, 0, 0], a=90)(screwhole("#8 Wood", wall_thickness + 1))
    ),
)

parts += [side_wall_base, front_wall, side_wall, floor, cut, holes]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

with open(__file__ + ".flipped.scad", "w") as f:
    f.write(scad_render(scale([-1, 1, 1])(union()(parts))))
