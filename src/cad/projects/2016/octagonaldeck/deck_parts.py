import functools
import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

# converts inches to feet
inches = lambda a: a / 12.0

side = 4
deck_height = 3.0
railing_height = 3.5
deck_board_width = inches(3.5)

lbs_pcf = 34.3353783

parts = []

cube_real = cube

weight = 0


def cube(*args, **kwargs):
    global weight
    r = cube_real(*args, **kwargs)
    weight += functools.reduce(lambda x, y: x * y, r.params["size"]) * lbs_pcf
    return r


def outer_horiz_supports():
    parts = []
    parts.append(
        translate([0, 0, deck_height - inches(5.5)])(
            cube([side, inches(1.5), inches(5.5)])
        )
    )

    parts.append(
        translate([0, side - inches(1.5), deck_height - inches(5.5)])(
            cube([side, inches(1.5), inches(5.5)])
        )
    )

    parts.append(
        translate([0, inches(1.5), deck_height - inches(5.5)])(
            cube([inches(1.5), side - inches(3), inches(5.5)])
        )
    )

    parts.append(
        translate([side - inches(1.5), inches(1.5), deck_height - inches(5.5)])(
            cube([inches(1.5), side - inches(3), inches(5.5)])
        )
    )

    # 16 inch separation
    parts.append(
        translate([inches(16 - 0.75), inches(1.5), deck_height - inches(5.5)])(
            cube([inches(1.5), side - inches(3), inches(5.5)])
        )
    )

    parts.append(
        translate([inches(32 - 0.75), inches(1.5), deck_height - inches(5.5)])(
            cube([inches(1.5), side - inches(3), inches(5.5)])
        )
    )

    return parts


def inner_horiz_supports():
    parts = []
    parts.append(
        translate([0, inches(3.5), deck_height - inches(5.5)])(
            cube([side, inches(1.5), inches(5.5)])
        )
    )

    parts.append(
        translate([0, side - inches(3.5 + 1.5), deck_height - inches(5.5)])(
            cube([side, inches(1.5), inches(5.5)])
        )
    )

    for i in range(3):
        sep_size = (side - inches(3.5 + 3.5)) / 4
        parts.append(
            translate([0, inches(3.5) + sep_size * (i + 1), deck_height - inches(5.5)])(
                cube([side, inches(1.5), inches(5.5)])
            )
        )

    parts.append(
        translate([inches(3.5), 0, deck_height - inches(5.5 + 5.5)])(
            cube([inches(1.5), side, inches(5.5)])
        )
    )

    parts.append(
        translate([side - inches(3.5 + 1.5), 0, deck_height - inches(5.5 + 5.5)])(
            cube([inches(1.5), side, inches(5.5)])
        )
    )

    return parts


def square_section(railing=None, outer_supports=True):
    parts = []

    # Posts
    offset = inches(1.5) if outer_supports else 0

    if railing == "left":
        p1h = deck_height + railing_height
        p2h = deck_height - inches(1.5)
        p3h = deck_height - inches(1.5)
        p4h = deck_height + railing_height
    elif railing == "right":
        p1h = deck_height - inches(1.5)
        p2h = deck_height + railing_height
        p3h = deck_height + railing_height
        p4h = deck_height - inches(1.5)
    elif railing == "back":
        p1h = deck_height + railing_height
        p2h = deck_height + railing_height
        p3h = deck_height - inches(1.5)
        p4h = deck_height - inches(1.5)
    elif railing == "forward":
        p1h = deck_height - inches(1.5)
        p2h = deck_height - inches(1.5)
        p3h = deck_height + railing_height
        p4h = deck_height + railing_height
    else:
        p1h = deck_height - inches(1.5)
        p2h = deck_height - inches(1.5)
        p3h = deck_height - inches(1.5)
        p4h = deck_height - inches(1.5)

    parts.append(translate([offset, offset, 0])(cube([inches(3.5), inches(3.5), p1h])))
    parts.append(
        translate([side - inches(3.5) - offset, offset, 0])(
            cube([inches(3.5), inches(3.5), p2h])
        )
    )
    parts.append(
        translate([side - inches(3.5) - offset, side - inches(3.5) - offset, 0])(
            cube([inches(3.5), inches(3.5), p3h])
        )
    )
    parts.append(
        translate([offset, side - inches(3.5) - offset, 0])(
            cube([inches(3.5), inches(3.5), p4h])
        )
    )

    # Horizontal Supports
    if outer_supports:
        parts += outer_horiz_supports()
    else:
        parts += inner_horiz_supports()

    # Floor
    board_count = int(side / inches(3.5))
    board_sep = (side - (deck_board_width * board_count)) / (board_count - 1)
    print(board_sep * 12)

    for i in range(board_count):
        parts.append(
            translate([0, i * (deck_board_width + board_sep), deck_height])(
                color((1, 0, 0))(cube([side, deck_board_width, inches(1.5)]))
            )
        )

    return parts


parts.append(square_section())
parts.append(right(side + inches(0.5))(square_section(railing="right")))
parts.append(left(side + inches(0.5))(square_section(railing="left")))
parts.append(forward(side + inches(0.5))(square_section(railing="forward")))
parts.append(back(side + inches(0.5))(square_section(railing="back")))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

print(weight)
