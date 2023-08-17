import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

size = 80
hole_dist = 9.5
thickness = 5

parts = []

side = intersection()(
    cube([size, size, thickness]), down(1)(cylinder(r=size, h=thickness + 2))
)
hole_positions = [
    [hole_dist + thickness, hole_dist + thickness],
    [size - 20, hole_dist + thickness],
    [hole_dist + thickness, size - 20],
]

for hole in hole_positions:
    side -= translate([hole[0], hole[1], -1])(
        cylinder(r=1.5, h=thickness + 2, segments=12)
    )

parts.append(side.copy())

parts.append(translate([0, thickness, 0])(rotate(v=[1, 0, 0], a=90)(side.copy())))

parts.append(translate([thickness, 0, 0])(rotate(v=[0, 1, 0], a=-90)(side.copy())))

parts = intersection()(union()(parts), sphere(size - 1))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
