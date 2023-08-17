import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.plan import *

circuit_board_size = Vec3(25.6, 34.2)  # TODO: set

box_inner_size = circuit_board_size.copy()
box_inner_size.z = 23  # TODO: set
box_inner_size += (1, 1, 0)  # Margin around circuit board

wall_thickness = 3


class ScrewHoleBlock(Part):
    block = CubePart(6, 6, 5).cut(Rod(r=1.5, h=5 + 0.1).translate(2.3 + 1, 2.3 + 1, 0))


class ButtonHole(Part):
    block = Rod(r=3, h=wall_thickness + 1, segments=24)
    inner = Rod(r=4, h=wall_thickness, segments=24).translate(
        0, 0, 0.5 + wall_thickness * 0.5
    )


class Button(Part):
    block = Rod(r=2.5, h=wall_thickness + 3, segments=24)
    inner = Rod(r=3.5, h=wall_thickness, segments=24)


class Box(Part):
    box = (
        Box(
            box_inner_size.x + wall_thickness * 2,
            box_inner_size.y + wall_thickness * 2,
            box_inner_size.z + wall_thickness,
            bottom=wall_thickness,
            left=wall_thickness,
            right=wall_thickness,
            front=wall_thickness,
            back=wall_thickness,
            top=0,
            roundover=2,
        )
        .cut(
            CubePart(15, 5, 10).translate(
                wall_thickness + box_inner_size.x * 0.5 - 7.5, -1, wall_thickness + 3
            )
        )
        .cut(
            CubePart(box_inner_size.x + 2, box_inner_size.y + 2, 3).translate(
                wall_thickness - 1,
                wall_thickness - 1,
                box_inner_size.z + wall_thickness - 2,
            )
        )
    )

    box.cut(
        ButtonHole()
        .rotate(v=[0, 1, 0], a=90)
        .translate(-0.5, wall_thickness + 4, wall_thickness + 17)
    )

    box.cut(
        ButtonHole()
        .rotate(v=[0, 1, 0], a=-90)
        .translate(
            box_inner_size.x + wall_thickness * 2,
            wall_thickness + 4,
            wall_thickness + 17,
        )
    )

    screw_hole_a = box.place_in_corner(ScrewHoleBlock(), 0, 0, 0)
    screw_hole_b = box.place_in_corner(ScrewHoleBlock(), 1, 0, 0)
    screw_hole_c = box.place_in_corner(ScrewHoleBlock(), 1, 1, 0)
    screw_hole_d = box.place_in_corner(ScrewHoleBlock(), 0, 1, 0)


box = Box()

button = Button()

box.render(__file__ + ".scad")
button.render(__file__ + "button.scad")
