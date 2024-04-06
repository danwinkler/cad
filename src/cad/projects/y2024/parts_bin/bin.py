import math
import random

from solid import (
    cube,
    cylinder,
    hole,
    hull,
    intersection,
    linear_extrude,
    polygon,
    rotate,
    scad_render,
    scale,
    sphere,
    translate,
    union,
)
from solid.utils import down

from cad.common.helper import Vec3

parts = []

# Small schaller bin interior is 68mm wide, 44 tall at the rim
# The walls are slightly sloped, so the bottom is a bit smaller


def _rounded_corner_box(width, length, depth, round_radius):
    corner_cyl = cylinder(r=round_radius, h=depth - round_radius, segments=32)
    corner_sphere = sphere(r=round_radius, segments=32)
    return hull()(
        translate([round_radius, round_radius, round_radius])(
            corner_cyl, corner_sphere
        ),
        translate([width - round_radius, round_radius, round_radius])(
            corner_cyl, corner_sphere
        ),
        translate([round_radius, length - round_radius, round_radius])(
            corner_cyl, corner_sphere
        ),
        translate([width - round_radius, length - round_radius, round_radius])(
            corner_cyl, corner_sphere
        ),
    )


def bin(
    width,
    length,
    depth,
    wall_thickness=1.5,
    bottom_thickness=1.5,
    round_radius=4,
    x_ribs=0,
    y_ribs=0,
):
    """
    Ribs are small rasied sections on the bottom of the bin that help prevent warping when printing
    """
    outer_box_shape = _rounded_corner_box(width, length, depth, round_radius)
    inner_box_shape = translate([wall_thickness, wall_thickness, bottom_thickness])(
        _rounded_corner_box(
            width - wall_thickness * 2,
            length - wall_thickness * 2,
            depth,
            round_radius - wall_thickness,
        )
    )

    box = outer_box_shape - inner_box_shape

    if x_ribs:
        for i in range(x_ribs):
            x_pos = (i + 1) * width / (x_ribs + 1)
            box += intersection()(
                translate([x_pos, 0, wall_thickness - 1])(
                    rotate([-90, 0, 0])(
                        cylinder(r=wall_thickness * 2, h=length, segments=32)
                    )
                ),
                outer_box_shape,
            )
            box -= translate([x_pos, 0, 0])(
                rotate([-90, 0, 0])(
                    cylinder(r=wall_thickness + 1, h=length, segments=32)
                )
            )

    return box


# parts.append(bin(width=33.5, length=33.5, depth=44))
parts.append(bin(width=67, length=33.5, depth=44, x_ribs=1))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
