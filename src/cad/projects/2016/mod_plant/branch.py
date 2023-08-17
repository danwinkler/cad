import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

stem_rad = 5

hole_depth = 10
hole_size = 2.5
hole_offset = 0.2


def branch(length, with_hole=False, with_nub=True):
    o = cylinder(r=stem_rad, h=length)
    if with_nub:
        o += up(length)(cylinder(r=hole_size, h=8, segments=36))
    if with_hole:
        o -= hole()(cylinder(r=hole_size + hole_offset, h=hole_depth, segments=36))
    return o


def typeA():
    o = branch(80, with_hole=True)

    for i in range(4):
        o += up(i * 20 + 5)(
            rotate(v=[0, 0, 1], a=(0 if (i % 2) == 0 else 180))(
                rotate(v=[0, 1, 0], a=45)(branch(30))
            )
        )

    return o


def base():
    o = branch(30, 0)
    o += cylinder(r=40, h=5)
    text_width = 47
    text_height = 7
    neg = []
    for x in range(-1, 2):
        for y in range(-6, 7):
            neg += [
                translate([x * text_width, y * text_height, -1])(
                    scale([-1, 1, 1])(
                        linear_extrude(height=2)(
                            text(
                                "Daniel Winkler",
                                size=5,
                                valign="center",
                                halign="center",
                                font="Arial",
                            )
                        )
                    )
                )
            ]
    o -= neg
    o += cylinder(r=40, h=5) - cylinder(r=38, h=5)
    return o


branch_types = [typeA, base]

print("Saving File")
for t in branch_types:
    with open(t.__name__ + ".scad", "w") as f:
        f.write(scad_render(t()))
