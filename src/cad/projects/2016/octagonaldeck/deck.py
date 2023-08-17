import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

# All units in Feet :/

show_fire_pit = True
show_level_1 = True
show_level_2 = True
show_level_3 = True

# converts inches to feet
inches = lambda a: a / 12.0

side = 6.0
support_rad = 0.5
support_height = 1.0
level_1_max_sep = inches(16)

fire_pit_radius = 2
fire_pit_height_above_deck = 2
fire_pit_wall_width = inches(8)

fire_pit_is_octagon = False
inside_supports = True

deck_height = 3.0
railing_height = 3.5  # 42 inches is international code apparently

first_level_support_size = inches(10)
second_level_support_size = inches(6)

first_support_height = (
    deck_height - first_level_support_size - second_level_support_size - inches(2)
)
second_support_height = first_support_height + first_level_support_size

radius = side * math.sqrt(4 + 2 * math.sqrt(2)) / 2
medium_diagonal = math.cos(math.pi * 2 / 8 * 0.5) * radius * 2

useable_radius = radius - fire_pit_radius - inches(5)
num_rings = int(useable_radius / inches(1 / (math.cos(math.pi * 0.125) / 6.1)))

rot_offset = 0.5
delta_a = 360.0 / 8
delta_a_rads = math.pi * 2 / 8

parts = []

# Fire Pit
if show_fire_pit:
    parts.append(
        rotate(rot_offset * delta_a)(
            color([0.5, 0.5, 0.6])(
                cylinder(
                    r=fire_pit_radius,
                    h=fire_pit_height_above_deck + deck_height,
                    segments=(8 if fire_pit_is_octagon else 20),
                )
                - up(fire_pit_height_above_deck + deck_height - 2)(
                    cylinder(r=fire_pit_radius - fire_pit_wall_width, h=10, segments=20)
                )
            )
        )
    )

# Concrete supports
for a in xrange(8):
    parts.append(
        rotate(a=(a + rot_offset) * delta_a)(
            right(radius)(
                color([1, 0, 0])(cylinder(r=support_rad, h=support_height, segments=8))
            )
        )
    )

if inside_supports:
    for x, y in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
        parts.append(
            translate([side / 2 * x, side / 2 * y, 0])(
                color([1, 0, 0])(cylinder(r=support_rad, h=support_height, segments=8)),
                translate([-inches(2), -inches(2), support_height])(
                    cube(
                        [
                            inches(4),
                            inches(4),
                            first_support_height
                            + first_level_support_size
                            - support_height,
                        ]
                    )
                ),
            )
        )

# Outer 4x4s
for a in xrange(8):
    x = cos((a + rot_offset) * delta_a_rads) * radius
    y = sin((a + rot_offset) * delta_a_rads) * radius
    parts.append(
        translate([x, y, 0])(
            translate([-inches(2), -inches(2), support_height])(
                cube(
                    [
                        inches(4),
                        inches(4),
                        deck_height + railing_height - support_height,
                    ]
                )
            )
        )
    )

# Y axis Supports
long_board_length = medium_diagonal + inches(4)
short_board_length = side + inches(4)
outer_board_length = medium_diagonal / 2 - side / 2
end_board_length = side + inches(8)
x_num_boards = int(short_board_length / level_1_max_sep) + 1
x_sep = short_board_length / x_num_boards
y_num_boards = int((medium_diagonal / 2 - side / 2) / level_1_max_sep) + 1
y_sep = (medium_diagonal / 2 - side / 2) / y_num_boards

if show_level_1:
    # Long

    parts.append(
        translate(
            [
                -side / 2 - inches(4),
                -medium_diagonal / 2 - inches(2),
                first_support_height,
            ]
        )(cube([inches(2), long_board_length, first_level_support_size]))
    )
    parts.append(
        translate(
            [
                side / 2 + inches(2),
                -medium_diagonal / 2 - inches(2),
                first_support_height,
            ]
        )(cube([inches(2), long_board_length, first_level_support_size]))
    )

    # Short
    parts.append(
        translate(
            [
                -medium_diagonal / 2 - inches(4),
                -side / 2 - inches(2),
                first_support_height,
            ]
        )(cube([inches(2), short_board_length, first_level_support_size]))
    )
    parts.append(
        translate(
            [
                medium_diagonal / 2 + inches(2),
                -side / 2 - inches(2),
                first_support_height,
            ]
        )(cube([inches(2), short_board_length, first_level_support_size]))
    )

    # X Axis Supports
    x_axis = []

    # Outer Boards
    x_axis.append(
        translate(
            [
                -medium_diagonal / 2 - inches(4),
                -side / 2 - inches(4),
                first_support_height,
            ]
        )(cube([outer_board_length, inches(2), first_level_support_size]))
    )

    x_axis.append(
        translate(
            [
                -medium_diagonal / 2 - inches(4),
                side / 2 + inches(2),
                first_support_height,
            ]
        )(cube([outer_board_length, inches(2), first_level_support_size]))
    )

    x_axis.append(
        translate(
            [
                medium_diagonal / 2 - outer_board_length + inches(4),
                -side / 2 - inches(4),
                first_support_height,
            ]
        )(cube([outer_board_length, inches(2), first_level_support_size]))
    )

    x_axis.append(
        translate(
            [
                medium_diagonal / 2 - outer_board_length + inches(4),
                side / 2 + inches(2),
                first_support_height,
            ]
        )(cube([outer_board_length, inches(2), first_level_support_size]))
    )

    # End Boards
    x_axis.append(
        translate(
            [
                -side / 2 - inches(4),
                -medium_diagonal / 2 - inches(4),
                first_support_height,
            ]
        )(cube([end_board_length, inches(2), first_level_support_size]))
    )

    x_axis.append(
        translate(
            [
                -side / 2 - inches(4),
                medium_diagonal / 2 + inches(2),
                first_support_height,
            ]
        )(cube([end_board_length, inches(2), first_level_support_size]))
    )

    # Inside Boards
    x_axis.append(
        translate([-side / 2 - inches(2), -side / 2 - inches(4), first_support_height])(
            cube([side + inches(4), inches(2), first_level_support_size])
        )
    )

    x_axis.append(
        translate([-side / 2 - inches(2), side / 2 + inches(2), first_support_height])(
            cube([side + inches(4), inches(2), first_level_support_size])
        )
    )

    # Dynamic Supports
    for i in xrange(1, x_num_boards):
        # Left
        x_axis.append(
            translate(
                [
                    -medium_diagonal / 2 - inches(2),
                    -side / 2 - inches(3) + i * x_sep,
                    first_support_height,
                ]
            )(
                cube(
                    [
                        outer_board_length - inches(2),
                        inches(2),
                        first_level_support_size,
                    ]
                )
            )
        )
        # Right
        x_axis.append(
            translate(
                [
                    medium_diagonal / 2 - outer_board_length + inches(4),
                    -side / 2 - inches(3) + i * x_sep,
                    first_support_height,
                ]
            )(
                cube(
                    [
                        outer_board_length - inches(2),
                        inches(2),
                        first_level_support_size,
                    ]
                )
            )
        )

    for i in xrange(1, y_num_boards):
        # Bottom
        x_axis.append(
            translate(
                [
                    -side / 2 - inches(2),
                    -medium_diagonal / 2 - inches(4) + i * y_sep,
                    first_support_height,
                ]
            )(cube([end_board_length - inches(4), inches(2), first_level_support_size]))
        )
        # Top
        x_axis.append(
            translate(
                [
                    -side / 2 - inches(2),
                    medium_diagonal / 2 + inches(2) - i * y_sep,
                    first_support_height,
                ]
            )(cube([end_board_length - inches(4), inches(2), first_level_support_size]))
        )

    parts.append(color([0, 1, 0])(union()(x_axis)))

# Second Level Supports
if show_level_2:

    def cross_piece(d):
        bsx = d
        bsy = 0
        bex = math.cos(math.pi * 0.125) * bsx
        bey = math.sin(math.pi * 0.125) * bsx
        return math.sqrt((bsx - bex) ** 2 + (bsy - bey) ** 2)

    board_length = cross_piece(fire_pit_radius + inches(2))
    o_board_length = cross_piece(medium_diagonal / 2)
    m_dist = (
        fire_pit_radius
        + inches(2)
        + (medium_diagonal / 2 - fire_pit_radius + inches(2)) * 0.5
    )
    m_board_length = cross_piece(m_dist)

    print(o_board_length)

    for a in xrange(8):
        # To corner
        parts.append(
            rotate(a=(a + rot_offset) * delta_a)(
                translate([fire_pit_radius + inches(2), 0, second_support_height])(
                    color([1, 1, 0])(
                        cube([useable_radius, inches(2), second_level_support_size])
                    )
                )
            )
        )

        # To face
        parts.append(
            rotate(a=(a) * delta_a)(
                translate([fire_pit_radius + inches(2), 0, second_support_height])(
                    color([1, 1, 0])(
                        cube(
                            [
                                medium_diagonal / 2 - fire_pit_radius + inches(2),
                                inches(2),
                                second_level_support_size,
                            ]
                        )
                    )
                )
            )
        )

    for a in xrange(16):
        # Small fillers
        parts.append(
            rotate(a=(a) * delta_a * 0.5 + delta_a * 0.25)(
                translate(
                    [
                        medium_diagonal / 2,
                        -o_board_length / 2 + inches(2),
                        second_support_height,
                    ]
                )(
                    color([1, 0.5, 0])(
                        cube(
                            [
                                inches(2),
                                o_board_length - inches(2),
                                second_level_support_size,
                            ]
                        )
                    )
                )
            )
        )

        # Small Fillers
        parts.append(
            rotate(a=(a) * delta_a * 0.5 + delta_a * 0.25)(
                translate(
                    [
                        fire_pit_radius + inches(2),
                        -board_length / 2 + inches(2),
                        second_support_height,
                    ]
                )(
                    color([1, 0.5, 0])(
                        cube(
                            [
                                inches(2),
                                board_length - inches(2),
                                second_level_support_size,
                            ]
                        )
                    )
                )
            )
        )

        # Medium Fillers
        parts.append(
            rotate(a=(a) * delta_a * 0.5 + delta_a * 0.25)(
                translate(
                    [m_dist, -m_board_length / 2 + inches(2), second_support_height]
                )(
                    color([1, 0.5, 0])(
                        cube(
                            [
                                inches(2),
                                m_board_length - inches(2),
                                second_level_support_size,
                            ]
                        )
                    )
                )
            )
        )

        # Third spike
        parts.append(
            rotate(a=(a) * delta_a * 0.5 + delta_a * 0.25)(
                translate([m_dist + inches(2), 0, second_support_height])(
                    color([1, 1, 0])(
                        cube(
                            [
                                medium_diagonal / 2 - m_dist - inches(2),
                                inches(2),
                                second_level_support_size,
                            ]
                        )
                    )
                )
            )
        )


if show_level_3:
    for r in xrange(num_rings):
        bsx = 0
        bsy = (
            fire_pit_radius
            + inches(2)
            + useable_radius
            - r * inches(1 / (math.cos(math.pi * 0.125) / 6.1))
        )
        bex = math.cos(math.pi * 0.25) * bsy
        bey = math.sin(math.pi * 0.25) * bsy
        board_length = math.sqrt((bsx - bex) ** 2 + (bsy - bey) ** 2)

        for a in xrange(8):
            # using some sweet SOHCAHTOA action to find the offset
            parts.append(
                rotate(a=(a + rot_offset) * delta_a)(
                    difference()(
                        translate(
                            [
                                fire_pit_radius
                                + inches(2)
                                + useable_radius
                                - r * inches(1 / (math.cos(math.pi * 0.125) / 6.1))
                                - inches(6),
                                0,
                                deck_height - inches(2),
                            ]
                        )(
                            rotate(a=22.5)(
                                color([0.7, 0.4, 0.2])(
                                    forward(-inches(2))(
                                        cube(
                                            [
                                                inches(6),
                                                board_length + inches(2),
                                                inches(2),
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
                        union()(back(inches(4.1))(cube([100, inches(5), 100]))),
                    )
                )
                - rotate(a=((a + 1) + rot_offset) * delta_a)(
                    forward(inches(0.4))(cube([10, inches(5 + 1), 6]))
                )
            )

print("Long Diagonal: " + str(radius))
print("Medium Diagonal: " + str(medium_diagonal))
print("Y Axis Long Support Length (x2)" + str(long_board_length))
print("Y Axis Short Support Length (x2)" + str(short_board_length))
print("X Axis Outer Support Length (x4)" + str(outer_board_length))
print("X Axis End Support Length (x2)" + str(end_board_length))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
