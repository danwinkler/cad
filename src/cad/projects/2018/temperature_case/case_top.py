import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

from .case import bottom_height

pin_length_in_inches = 3.0 / 8.0

board_width_in_inches = 1.7
board_length_in_inches = 1.4
y_board_margin = 0.05
x_board_margin = 0.5
width_in_inches = board_width_in_inches + x_board_margin * 2
length_in_inches = board_length_in_inches + y_board_margin * 2

hole_offset_in_inches = 0.1
hole_size_in_inches = 0.11
round_over = 0.1

top_height = 0.25

parts = []


def case_hole():
    height = (top_height - round_over) + (5.0 / 16.0)
    return (
        translate([-(hole_offset_in_inches), -(hole_offset_in_inches), 0])(
            cube([hole_offset_in_inches * 2, hole_offset_in_inches, height]),
            cube([hole_offset_in_inches, hole_offset_in_inches * 2, height]),
        )
        + cylinder(r=hole_offset_in_inches, h=height, segments=24)
    ) + hole()(
        down(round_over + 0.1)(
            cylinder(r=hole_size_in_inches * 0.5, h=height + 0.3, segments=24)
        )
    )


@in_inches
def case():
    outer_case = (
        minkowski()(
            translate([round_over, round_over, round_over])(
                cube([width_in_inches, length_in_inches + 0.2, top_height])
            ),
            sphere(round_over, segments=12),
        )
        - translate([round_over, round_over, round_over])(
            cube([width_in_inches, length_in_inches, top_height + round_over * 2])
        )
        - translate([0, 0, top_height])(
            cube(
                [
                    width_in_inches + round_over * 2,
                    length_in_inches + round_over * 2 + 0.2,
                    round_over * 2,
                ]
            )
        )
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

    screen_hole = translate(
        [
            round_over + width_in_inches - 1 - 0.2,
            round_over + length_in_inches * 0.5 - 0.5,
            -0.1,
        ]
    )(hole()(cube([1, 1, 1])))

    temp_slot = translate(
        [
            (round_over * 2 + width_in_inches)
            - (round_over + width_in_inches * 0.5 - 0.9),
            round_over + length_in_inches + round_over,
            top_height - (1.0 / 8.0),
        ]
    )(hole()(translate([-0.60 - 1.02, 0, 0])(cube([1.02, (1.0 / 16.0), 0.2]))))

    return union()([outer_case, case_holes, screen_hole, temp_slot])


parts.append(case())


if __name__ == "__main__":
    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(scad_render(union()(parts)))
