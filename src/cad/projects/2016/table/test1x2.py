"""
Test 1:
    Printed holes vertically. 19mmx38mm. Margins were .05, .1 and .15 on all side (so hole was x+margin*2,y+margin*2).
    .05 was very snug. .1 was a good fit. .15 fit well, but slides easily along.
    Because holes were printed vertically, there was some material that encroached on the hole which
    made the smaller holes impossible to slide fully down the material (1x2 pine). The largest hole could fit fully
    when force was applied.


"""


import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

inner_x = 19
inner_y = 38

height = 20

offset = 0.1
offsets = [0.05, 0.1, 0.15]

wall_thickness = 4

parts = []

base_width = (
    (wall_thickness + inner_x) * len(offsets) + wall_thickness + sum(offsets) * 2
)
b = cube([base_width, inner_y + wall_thickness * 2 + (max(offsets) * 2), height])

offset_accum = wall_thickness
for i, o in enumerate(offsets):
    x_off = offset_accum
    b -= translate([x_off, wall_thickness, 0])(
        cube([inner_x + o * 2, inner_y + o * 2, height])
    )
    offset_accum += inner_x + o * 2 + wall_thickness


parts += [b]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
