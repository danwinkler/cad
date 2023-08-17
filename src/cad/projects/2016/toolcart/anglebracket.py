import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wall_thickness = 4

offset = 0.15

inner_x = 19 + offset * 2
inner_y = 38 + offset * 2

length = 60

lip_size = 20

outer_x = inner_x + wall_thickness * 2
outer_y = inner_y + wall_thickness * 2

parts = []

parts += [
    translate([0, 0, 0])(
        rotate(a=36.87, v=[1, 0, 0])(
            down(50)(
                cube([outer_x, outer_y, 100]),
                hole()(
                    translate([wall_thickness, -1, 0])(
                        cube([inner_x, inner_y + wall_thickness + 1, 100])
                    )
                ),
            ),
            hole()(
                translate([outer_x / 2.0, outer_y, -20])(
                    rotate(a=-90, v=[1, 0, 0])(screwhole("#8 Wood", wall_thickness + 1))
                )
            ),
        )
    ),
    translate([outer_x, 0, 0])(cube([lip_size, outer_y, wall_thickness])),
    hole()(
        translate([0, outer_y * 0.33, outer_x * 0.5])(
            rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", outer_x + 1))
        ),
        translate([0, outer_y * 0.66, outer_x * 0.5])(
            rotate(a=-90, v=[0, 1, 0])(screwhole("#8 Wood", outer_x + 1))
        ),
        translate([outer_x + lip_size * 0.5, outer_y * 0.5, 0])(
            rotate(a=180, v=[0, 1, 0])(screwhole("#8 Wood", wall_thickness + 1))
        ),
    ),
]

parts += [
    hole()(
        translate([-100, -100, -100])(cube([200, 200, 100])),
        translate([-100, -100, outer_x - wall_thickness])(cube([200, 200, 100])),
    )
]


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

with open(__file__ + ".flipped.scad", "w") as f:
    f.write(scad_render(scale([-1, 1, 1])(union()(parts))))
