import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.premade import *

mm_in_inches = 25.4
wall_thickness = 2
rim_width = 8


def rim(diameter, depth):
    rad = diameter * 0.5
    return union()(
        cylinder(r=rad + rim_width, h=wall_thickness, segments=60),
        cylinder(r=rad, h=depth + wall_thickness, segments=60),
        hole()(
            down(1)(
                cylinder(
                    r=rad - wall_thickness, h=depth + wall_thickness + 2, segments=60
                )
            )
        ),
    )


def cup(diameter, depth):
    rad = diameter * 0.5
    wall_height = max(depth - rad, 0)
    return union()(
        cylinder(r=rad + rim_width, h=wall_thickness, segments=60),
        cylinder(r=rad, h=wall_height + wall_thickness, segments=60),
        up(wall_height + wall_thickness)(sphere(r=rad, segments=60)),
        hole()(
            down(1)(
                cylinder(r=rad - wall_thickness, h=wall_height + wall_thickness + 1)
            ),
            up(wall_height + wall_thickness)(
                sphere(r=rad - wall_thickness, segments=60)
            ),
        ),
    )


def save(filename, thing):
    print("Saving File " + filename)
    with open(filename + ".scad", "w") as f:
        f.write(scad_render(union()(thing)))


save("rim2", rim(mm_in_inches * 2, mm_in_inches * 0.75 + 1))
save("rim1.5", rim(mm_in_inches * 1.5, mm_in_inches * 0.75 + 1))
save("rim1", rim(mm_in_inches * 1, mm_in_inches * 0.75 + 1))
save("rim.75", rim(mm_in_inches * 0.75, mm_in_inches * 0.75 + 1))
save("rim1.125", rim(mm_in_inches * 1.125, mm_in_inches * 0.75 + 1))
save("rim.875", rim(mm_in_inches * 0.875, mm_in_inches * 0.75 + 1))
save("cup2_3", cup(mm_in_inches * 2, mm_in_inches * 3))
save("cup1.5_3", cup(mm_in_inches * 1.5, mm_in_inches * 3))
save("cup1.125_3.5", cup(mm_in_inches * 1.125, mm_in_inches * 3.5))
