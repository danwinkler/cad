import math
import random
from dataclasses import dataclass

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

ring_rad = 500
ring_depth = 80
ring_width = 50

outer = cylinder(r=ring_rad, h=ring_width)
inner = down(1)(cylinder(r=ring_rad - ring_depth, h=ring_width + 2))

ring = rotate(a=45, v=[0, 1, 0])(outer - inner)

for i in [0, 120, 240]:
    parts.append(
        rotate(a=i, v=[0, 0, 1])(
            translate([0, ring_rad, 0])(
                rotate(a=-60, v=[0, 0, 1])(translate([0, -ring_rad, 0])(ring))
            )
        )
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
