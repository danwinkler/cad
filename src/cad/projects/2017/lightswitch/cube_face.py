import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

from . import lightswitch as ls

parts = []

parts.append(ls.face)

cube_size = 5

x_count = int(ls.fx / cube_size)
y_count = int(ls.fy / cube_size)

x_offset = (ls.fx - x_count * cube_size) * 0.5
y_offset = (ls.fy - y_count * cube_size) * 0.5

cubes = []

for x in range(x_count):
    for y in range(y_count):
        ox = x * cube_size - ls.fx * 0.5
        oy = y * cube_size - ls.fy * 0.5
        ov = Vec3(ox, oy)
        ov.normalize()
        cubes.append(
            translate([x * cube_size, y * cube_size, 1.9])(
                multmatrix(
                    [[1, 0, ov.x, 0], [0, 1, ov.y, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
                )(cube([cube_size, cube_size, random.normalvariate(3, 1)]))
            )
        )

parts.append(translate([x_offset, y_offset, 0])(cubes))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
