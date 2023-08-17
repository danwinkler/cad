import math
import random

from solid import (
    cube,
    cylinder,
    hole,
    intersection,
    linear_extrude,
    polygon,
    rotate,
    scad_render,
    scale,
    translate,
    union,
)
from solid.utils import down

from cad.common.helper import Vec3

parts = []

angle = 15
side_length = 50
height = 15
screw_hole_rad = 2
screw_head_rad = 4.4
screw_transition_length = 3

# Create a triangle
triangle_side_scalar = 2
base = linear_extrude(height)(
    polygon(
        points=[
            [0, 0],
            [
                math.cos(math.radians(angle / 2)) * side_length * triangle_side_scalar,
                math.sin(math.radians(angle / 2)) * side_length * triangle_side_scalar,
            ],
            [
                -math.cos(math.radians(angle / 2)) * side_length * triangle_side_scalar,
                math.sin(math.radians(angle / 2)) * side_length * triangle_side_scalar,
            ],
        ]
    )
)

base = intersection()(
    base,
    cylinder(r=side_length, h=height, segments=64),
)

base = base - translate([0, side_length * 2 + 7, 2])(
    cylinder(r=side_length * 2, h=height - 4, segments=64)
)

for side in [-1, 1]:
    cutout = (
        cylinder(r=screw_hole_rad, h=height + 1, segments=16)
        + cylinder(r=screw_head_rad, h=4, segments=16)
        + translate([0, 0, 4 - 0.001])(
            cylinder(
                r1=screw_head_rad,
                r2=screw_hole_rad,
                h=screw_transition_length,
                segments=16,
            )
        )
    )

    for d in [15, 35]:
        rot_vec = Vec3(
            math.cos(math.radians(angle / 2)) * side,
            math.sin(math.radians(angle / 2)),
            0,
        )
        rot_vec.normalize()
        base -= translate(
            [
                math.cos(math.radians(angle / 2)) * side * d,
                math.sin(math.radians(angle / 2)) * d,
                height / 2,
            ]
        )(
            rotate(
                a=90 * side,
                v=rot_vec.to_list(),
            )(down(9)(cutout))
        )

parts.append(base)


def half_cyl():
    return cylinder(r=5, h=height, segments=10) - translate([-8, -8, -1])(
        cube([16, 8, height + 2])
    )


overhang_support = translate([0, 4, 0])(
    rotate(v=[1, 0, 0], a=-15)(half_cyl())
) + translate([0, 4, height])(scale([1, 1, -1])(rotate(v=[1, 0, 0], a=-15)(half_cyl())))

parts.append(overhang_support)

top_bottom_clear = hole()(
    translate([-100, -100, height])(cube([200, 200, height]))
    + translate([-100, -100, -height])(cube([200, 200, height]))
)

parts.append(top_bottom_clear)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
