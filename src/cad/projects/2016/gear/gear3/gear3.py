import math
import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

parts.append(cube([60, 20, 4]))
parts.append(
    translate([10, 10, 0])(
        union()(
            cylinder(h=10, r=3.5), translate([20.555 * 2, 0, 0])(cylinder(h=10, r=3.5))
        )
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
