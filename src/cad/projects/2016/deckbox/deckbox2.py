import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

width = 73
height = 100
length = 47
wall_thickness = 5
top_buffer = 3
slide_margin = 1
slide_cut = 3
slide_extra = 2

parts = []

# main body
body = cube(
    [
        width + wall_thickness * 2,
        length + wall_thickness * 2,
        height
        + wall_thickness
        + top_buffer
        + slide_margin
        + wall_thickness
        + wall_thickness,
    ]
)
# cut out inside
body -= translate([wall_thickness, wall_thickness, wall_thickness])(
    cube([width, length, 1000])
)
# cut out slide area
body -= translate(
    [wall_thickness - slide_cut, -1, wall_thickness + height + top_buffer]
)(
    cube(
        [
            width + slide_cut * 2,
            length + wall_thickness + slide_cut + 1,
            wall_thickness + slide_margin,
        ]
    )
)
# cut off crossbar
body -= translate([wall_thickness, -1, wall_thickness + height + top_buffer])(
    cube([width, wall_thickness + 2, 100])
)

slide = cube([width + slide_extra * 2, length + slide_extra, wall_thickness])

parts.append(body)
parts.append(left(width + 10)(slide))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
