import math

from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *

in_to_mm = 25.4

insert_hole_rad = 12.75 / 2
wood_width = 1.5 * in_to_mm
wood_height = 3.5 * in_to_mm
wall_thickness = 10
base_thickness = 26
part_height = base_thickness + 40

hole_locations = [
    wood_height - 1 * in_to_mm,
    wood_height - 2 * in_to_mm,
]

hole_shape = cylinder(r=6, h=base_thickness + 2, segments=90) + cylinder(
    r=insert_hole_rad, h=base_thickness - 12, segments=90
)


def build_part():
    base = cube(
        [
            wood_width + wall_thickness * 2,
            wood_height + wall_thickness * 2,
            base_thickness,
        ]
    )

    rounded_corner_rad = 5

    part = minkowski()(
        translate([rounded_corner_rad, rounded_corner_rad, rounded_corner_rad])(
            cube(
                [
                    wood_width + wall_thickness * 2 - rounded_corner_rad * 2,
                    wood_height + wall_thickness * 2 - rounded_corner_rad * 2,
                    part_height - rounded_corner_rad,
                ]
            )
        ),
        sphere(r=rounded_corner_rad, segments=36),
    )

    # left wall
    # part += translate([0, 0, 0])(
    #     cube([wall_thickness, wood_height + wall_thickness * 2, part_height])
    # )

    # # right wall
    # part += translate([wood_width + wall_thickness, 0, 0])(
    #     cube([wall_thickness, wood_height + wall_thickness * 2, part_height])
    # )

    # # Front wall (double thickness because we're going to cut it back a bit)
    # part += translate([0, 0, 0])(
    #     cube([wood_width + wall_thickness * 2, wall_thickness * 2, part_height])
    # )

    # Cut out angle from front wall
    part -= (
        translate([wall_thickness, wall_thickness, base_thickness])(
            rotate(a=-7.5, v=[1, 0, 0])(
                cube([wood_width, wood_height * 2, part_height])
            )
        )
        - base
    )

    # Cut out holes
    for hole_location in hole_locations:
        part -= translate(
            [wall_thickness + wood_width / 2, wall_thickness + hole_location, -1]
        )(hole_shape)

    return part


parts = []

parts.append(build_part())

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
