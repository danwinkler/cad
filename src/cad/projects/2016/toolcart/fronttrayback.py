import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wall_thickness = 4

inner_x = 19
inner_y = 38

length = 45

depth = 30

outer_x = inner_x + wall_thickness * 2
outer_y = inner_y + wall_thickness * 2

height_offset = 18

parts = []

side_wall = cube(
    [
        wall_thickness + inner_x + length,
        wall_thickness + height_offset + inner_x + wall_thickness,
        wall_thickness,
    ]
)
side_wall += cube(
    [outer_x, wall_thickness + height_offset + inner_x + height_offset, wall_thickness]
)

a = translate([0, 0, wall_thickness])(
    cube(
        [
            wall_thickness,
            wall_thickness + height_offset + inner_x + height_offset,
            depth,
        ]
    )
)

b = translate([0, 0, wall_thickness])(cube([outer_x, wall_thickness, depth]))

c = translate([wall_thickness + inner_x, 0, wall_thickness])(
    cube([wall_thickness, wall_thickness + height_offset, depth])
)

d = translate([wall_thickness + inner_x, height_offset, wall_thickness])(
    cube([length * 0.5, wall_thickness, depth])
)

e = translate(
    [wall_thickness + inner_x, wall_thickness + height_offset + inner_x, wall_thickness]
)(cube([wall_thickness, height_offset, depth]))

f = translate(
    [wall_thickness + inner_x, wall_thickness + height_offset + inner_x, wall_thickness]
)(cube([length * 0.5, wall_thickness, depth]))

holes = hole()(
    translate([outer_x * 0.5, 0, wall_thickness + depth * 0.5])(
        rotate(a=90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
    ),
    translate(
        [
            0,
            wall_thickness + height_offset + inner_x * 0.5,
            wall_thickness + depth * 0.5,
        ]
    )(rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))),
)

parts += [side_wall, a, b, c, d, e, f, holes]


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

with open(__file__ + ".flipped.scad", "w") as f:
    f.write(scad_render(scale([-1, 1, 1])(union()(parts))))
