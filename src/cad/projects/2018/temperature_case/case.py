import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

from .base_plug import pin_holes

pin_length_in_inches = 3.0 / 8.0

board_width_in_inches = 1.7
board_length_in_inches = 1.4
y_board_margin = 0.05
x_board_margin = 0.5
width_in_inches = board_width_in_inches + x_board_margin * 2
length_in_inches = board_length_in_inches + y_board_margin * 2

bottom_height = 1.4
hole_offset_in_inches = 0.1
hole_size_in_inches = 0.11
round_over = 0.1

plug_height = 1
plug_rad = 0.25

parts = []


def screw_hole():
    return (
        translate(
            [
                -(hole_offset_in_inches + x_board_margin),
                -(hole_offset_in_inches + y_board_margin),
                0,
            ]
        )(
            cube(
                [
                    x_board_margin + hole_offset_in_inches * 2,
                    y_board_margin + hole_offset_in_inches,
                    pin_length_in_inches,
                ]
            ),
            cube(
                [
                    x_board_margin + hole_offset_in_inches,
                    y_board_margin + hole_offset_in_inches * 2,
                    pin_length_in_inches,
                ]
            ),
        )
        + cylinder(r=hole_offset_in_inches, h=pin_length_in_inches, segments=24)
    ) - cylinder(r=hole_size_in_inches * 0.5, h=pin_length_in_inches + 0.1, segments=24)


def case_hole():
    height = bottom_height - (round_over + 0.3)
    return (
        translate(
            [
                -(hole_offset_in_inches + y_board_margin),
                -(hole_offset_in_inches + y_board_margin),
                0,
            ]
        )(
            cube(
                [
                    y_board_margin + hole_offset_in_inches * 2,
                    y_board_margin + hole_offset_in_inches,
                    height,
                ]
            ),
            cube(
                [
                    y_board_margin + hole_offset_in_inches,
                    y_board_margin + hole_offset_in_inches * 2,
                    height,
                ]
            ),
        )
        + cylinder(r=hole_offset_in_inches, h=height, segments=24)
    ) + hole()(cylinder(r=hole_size_in_inches * 0.5, h=height + 0.1, segments=24))


def vents():
    parts = [
        translate([-round_over - 0.1, length_in_inches * 0.5 - 0.3 + 0.2 * i, 0.2])(
            minkowski()(
                cube([round_over + 0.2, 0.1 - 0.06, 0.7]),
                rotate(a=90, v=[0, 1, 0])(cylinder(r=0.03, h=0.001, segments=12)),
            )
        )
        for i in range(4)
    ]
    return hole()(parts)


@in_inches
def case():
    outer_case = (
        minkowski()(
            translate([round_over, round_over, round_over])(
                cube([width_in_inches, length_in_inches, bottom_height])
            ),
            sphere(round_over, segments=12),
        )
        - translate([round_over, round_over, round_over])(
            cube([width_in_inches, length_in_inches, bottom_height + round_over * 2])
        )
        - translate([0, 0, bottom_height])(
            cube(
                [
                    width_in_inches + round_over * 2,
                    length_in_inches + round_over * 2,
                    round_over * 2,
                ]
            )
        )
        - translate(
            [
                round_over + width_in_inches * 0.5 - 0.8,
                round_over + length_in_inches - 0.01,
                round_over + 0.5,
            ]
        )(cube([0.5, round_over + 0.02, 1]))
    )

    pins = translate(
        [round_over + x_board_margin, round_over + y_board_margin, round_over]
    )(
        translate([0.45, 0.1, 0])(pin_holes(12)),
        translate([1.15, 0.1, 0])(pin_holes(12)),
    )

    screw_holes = translate(
        [round_over + x_board_margin, round_over + y_board_margin, round_over]
    )(
        translate([hole_offset_in_inches, hole_offset_in_inches, 0])(screw_hole()),
        translate(
            [board_width_in_inches - hole_offset_in_inches, hole_offset_in_inches, 0]
        )(scale([-1, 1, 1])(screw_hole())),
        translate(
            [
                board_width_in_inches - hole_offset_in_inches,
                board_length_in_inches - hole_offset_in_inches,
                0,
            ]
        )(scale([-1, -1, 1])(screw_hole())),
        translate(
            [hole_offset_in_inches, board_length_in_inches - hole_offset_in_inches, 0]
        )(scale([1, -1, 1])(screw_hole())),
    )

    case_holes = translate([round_over, round_over, round_over])(
        translate([hole_offset_in_inches, hole_offset_in_inches, 0])(case_hole()),
        translate([width_in_inches - hole_offset_in_inches, hole_offset_in_inches, 0])(
            scale([-1, 1, 1])(case_hole())
        ),
        translate(
            [
                width_in_inches - hole_offset_in_inches,
                length_in_inches - hole_offset_in_inches,
                0,
            ]
        )(scale([-1, -1, 1])(case_hole())),
        translate([hole_offset_in_inches, length_in_inches - hole_offset_in_inches, 0])(
            scale([1, -1, 1])(case_hole())
        ),
    )

    plug_hole = hole()(
        translate([round_over + width_in_inches * 0.5, -0.1, plug_height])(
            rotate(a=-90, v=[1, 0, 0])(
                cylinder(h=round_over + 0.2, r=plug_rad, segments=24)
            )
        )
    )

    vent = translate([round_over, round_over, round_over])(
        vents(), right(width_in_inches)(vents())
    )

    temp_slot = translate(
        [
            round_over + width_in_inches * 0.5 - 0.9,
            round_over + length_in_inches + round_over,
            round_over + 0.4,
        ]
    )(
        hull()(
            cube([1.8, 0.2, 0.1]), translate([0, -0.01, -0.4])(cube([1.8, 0.01, 0.01]))
        )
        - translate([0.60, 0, 0])(cube([1.02, (1.0 / 16.0), 0.2]))
        + translate()(cube([0.1, 0.2, bottom_height - (round_over + 0.4)]))
        + translate([1.7, 0, 0])(cube([0.1, 0.2, bottom_height - (round_over + 0.4)]))
    )

    return union()(
        [outer_case, pins, screw_holes, case_holes, plug_hole, vent, temp_slot]
    )


parts.append(case())


if __name__ == "__main__":
    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(scad_render(union()(parts)))
