from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

wood_thickness = 5.5
wall_thickness = 3

height = 12
length = 25
lip = 15

bod_size = wall_thickness * 2 + wood_thickness
lengthplusbody = length + bod_size

parts = [
    # outer walls
    cube([length, wall_thickness, height + wall_thickness]),
    # inner walls
    translate([0, wall_thickness + wood_thickness, 0])(
        cube([length, wall_thickness, height + wall_thickness]),
    ),
    # bridges
    up(height)(
        translate([0, 0, 0])(
            cube([length, wall_thickness * 2 + wood_thickness, wall_thickness])
        )
    ),
    # floor
    translate([0, bod_size, 0])(cube([length, lip, wall_thickness])),
    # screw holes
    translate([length * 0.5, 0, height * 0.5])(
        rotate(a=90, v=[1, 0, 0])(screwhole("#8 Wood", bod_size + 1))
    ),
    translate([length * 0.5, bod_size + lip * 0.5, wall_thickness + 5])(
        screwhole("#8 Wood", wall_thickness + 6)
    ),
]


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
