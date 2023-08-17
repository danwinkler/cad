import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

inner_x = 19
inner_y = 38

offset = 0.15

wall_thickness = 4

height = 40

angle_in_degrees = 10

inner_total_x = inner_x + offset * 2
inner_total_y = inner_y + offset * 2

cube_x = inner_total_x + wall_thickness * 2
cube_y = inner_total_y + wall_thickness * 2

inches_in_mm = 25.4
half_in = inches_in_mm / 2.0
size = half_in + 0.5
rad = size / 2

hole_size_inner = 1.9
hole_shaft_length = wall_thickness * 6

screwhole = (
    down(hole_shaft_length)(
        cylinder(r=hole_size_inner, h=hole_shaft_length + wall_thickness, segments=12)
    )
    + up(wall_thickness - 3)(cylinder(r1=hole_size_inner, r2=4, h=3, segments=12))
    + up(wall_thickness)(cylinder(r=4, h=3, segments=12))
)

parts = []


def cbox(v):
    return translate([-v[0] / 2.0, -v[1] / 2.0, 0])(cube(v))


sheath = (
    translate([0, 0, -10])(
        rotate(a=angle_in_degrees, v=[0, 1, 0])(cbox([cube_x, cube_y, height + 20]))
    )
    - down(20)(cbox([100, 100, 20]))
    - up(height)(cbox([100, 100, 20]))
)

cutaway = translate([0, 0, -10])(
    rotate(a=angle_in_degrees, v=[0, 1, 0])(
        translate([wall_thickness - cube_x / 2.0, wall_thickness - cube_y / 2.0, 18])(
            cube([inner_total_x, inner_total_y, height + 20])
        )
    )
)

angles_width = rad * 2 + wall_thickness * 2
angles_length = 40
hole_depth = 30

angles_pieces = translate([0, cube_y / 2.0, 0])(
    rotate(a=-45, v=[0, 0, 1])(
        translate([0, 0, 0])(
            cube([angles_width, angles_length, height])
            - translate([0, angles_length, 0])(
                hole()(
                    translate([angles_width / 2.0, 1, height / 2.0])(
                        rotate(a=90, v=[1, 0, 0])(cylinder(r=rad, h=hole_depth + 1))
                    )
                    + translate(
                        [angles_width / 2.0, -hole_depth / 2.0, wall_thickness]
                    )(rotate(v=[1, 0, 0], a=180)(screwhole))
                )
            )
        )
    )
) + translate([0, -cube_y / 2.0, 0])(
    rotate(a=45, v=[0, 0, 1])(
        translate([0, -angles_length, 0])(
            cube([angles_width, angles_length, height])
            - hole()(
                translate([angles_width / 2.0, -1, height / 2.0])(
                    rotate(a=-90, v=[1, 0, 0])(cylinder(r=rad, h=hole_depth + 1))
                )
                + translate([angles_width / 2.0, hole_depth / 2.0, wall_thickness])(
                    rotate(v=[1, 0, 0], a=180)(screwhole)
                )
            )
        )
    )
)


parts.append(sheath - cutaway)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
