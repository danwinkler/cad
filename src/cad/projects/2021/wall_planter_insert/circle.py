import math
import random
from dataclasses import dataclass

from solid import *
from solid.utils import *

from lib.helper import *

"""
Large internal radius 18 7/8“
Lip internal offset 7 1/2“
Small internal radius 15“
Small internal offset 16 1/8“
internal depth (from back to front) 2 7/8 for both

Planters:
A: Large black
B: small white
C: small black
D: large white
"""

in_to_mm = 25.4


@dataclass
class Planter:
    rad: float
    depth: float  # Inner depth from back to front
    z_offset: float  # Distance from inner bottom to top of lip
    cyl_bevel: float = 0  # Cylinder bevel


a_planter = Planter(
    rad=18.75 * 0.5 * in_to_mm, depth=2.75 * in_to_mm, z_offset=7.5 * in_to_mm
)
b_planter = Planter(
    rad=15 * 0.5 * in_to_mm, depth=2.9 * in_to_mm, z_offset=6 * in_to_mm
)
c_planter = Planter(
    rad=14.875 * 0.5 * in_to_mm, depth=2.5 * in_to_mm, z_offset=6 * in_to_mm
)
d_planter = Planter(
    rad=18.875 * 0.5 * in_to_mm,
    depth=3.375 * in_to_mm,
    z_offset=7.75 * in_to_mm,
    cyl_bevel=15,
)


large_inner_diameter = 18.875 * in_to_mm
large_inner_rad = large_inner_diameter / 2
large_inner_depth = 2.875 * in_to_mm
large_lip_offset = 7.5 * in_to_mm
pot_depth = 4 * in_to_mm
segments = 128

wall_thickness = 2

hole_size = 10


def get_cylinder(rad, depth, bevel):
    return up(rad)(
        rotate(v=[1, 0, 0], a=-90)(
            minkowski()(
                up(bevel)(
                    cylinder(
                        r=rad - bevel,
                        h=depth - (bevel * 2),
                        segments=segments,
                    )
                ),
                sphere(r=bevel),
            )
        )
    )


def left_box(planter: Planter, x_offset, pot_depth):
    left_edge_bottom = (
        math.cos(math.asin(1 - ((planter.z_offset - pot_depth) / planter.rad)))
        * planter.rad
    )

    cyl = get_cylinder(planter.rad, planter.depth, planter.cyl_bevel)

    front = intersection()(
        translate([-planter.rad, 0, planter.z_offset - pot_depth])(
            cube([planter.rad + x_offset, wall_thickness, pot_depth])
        ),
        cyl,
    )

    back = intersection()(
        translate(
            [-planter.rad, planter.depth - wall_thickness, planter.z_offset - pot_depth]
        )(cube([planter.rad + x_offset, wall_thickness, pot_depth])),
        cyl,
    )
    right = translate([x_offset - wall_thickness, 0, planter.z_offset - pot_depth])(
        cube([wall_thickness, planter.depth, pot_depth])
    )
    left = intersection()(
        cyl
        - up(wall_thickness)(
            forward(wall_thickness)(
                get_cylinder(
                    planter.rad - wall_thickness,
                    planter.depth - wall_thickness * 2,
                    planter.cyl_bevel - wall_thickness,
                )
            )
        ),
        translate([-planter.rad, 0, planter.z_offset - pot_depth])(
            cube([planter.rad + x_offset, planter.depth, pot_depth])
        ),
    )
    bottom = intersection()(
        translate([-planter.rad, 0, planter.z_offset - pot_depth])(
            cube([planter.rad + x_offset, planter.depth, wall_thickness])
        ),
        cyl,
    )

    hole_block = cube([hole_size, hole_size, hole_size])

    holes = [
        translate([x_offset - hole_size * 2, 0, planter.z_offset - pot_depth])(
            hole_block
        ),
        translate(
            [
                x_offset - hole_size * 2,
                planter.depth - hole_size,
                planter.z_offset - pot_depth,
            ]
        )(hole_block),
        translate([-left_edge_bottom + hole_size, 0, planter.z_offset - pot_depth])(
            hole_block
        ),
        translate(
            [
                -left_edge_bottom + hole_size,
                planter.depth - hole_size,
                planter.z_offset - pot_depth,
            ]
        )(hole_block),
    ]

    return union()(front, back, right, left, bottom) - holes


def support(planter, pot_depth):
    z_offset = planter.z_offset - pot_depth
    cyl = get_cylinder(planter.rad, planter.depth, planter.cyl_bevel)

    solid = intersection()(
        translate([-planter.rad, 0, 0])(cube([planter.rad, planter.depth, z_offset])),
        cyl,
    )

    holes = []

    hole_rad = 15
    hole_spacing = hole_rad * 2 + 10
    for i in range(-int(planter.rad), hole_spacing, hole_spacing):
        holes.append(translate([i, 0, 0])(cylinder(r=hole_rad, h=z_offset + 1)))
        holes.append(
            translate([i, planter.depth, 0])(cylinder(r=hole_rad, h=z_offset + 1))
        )

    return solid - holes


parts = []

parts.append(
    left_box(
        d_planter,
        x_offset=-0,
        pot_depth=pot_depth,
    )
)

# parts.append(
#     support(
#         d_planter,
#         pot_depth=pot_depth,
#     )
# )


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
