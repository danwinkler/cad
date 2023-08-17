import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

random.seed(4)

width = 40
length = 40

border_size = 2
base_thickness = 2

support_size = 4
support_sep = 8
support_height = 1.5

support_num_x = ((width - support_size) / (support_size + support_sep)) + 1
support_num_y = ((length - support_size) / (support_size + support_sep)) + 1

for x in range(support_num_x):
    for y in range(support_num_y):
        parts.append(
            translate(
                [x * (support_size + support_sep), y * (support_size + support_sep), 0]
            )(cube([support_size, support_size, support_height]))
        )

for x in range(support_num_x):
    parts.append(
        translate([x * (support_size + support_sep), 0, support_height - 0.5])(
            cube([support_size, length, 0.5])
        )
    )

    """
for y in range( support_num_y ):
	parts.append(
		translate( [0, y*(support_size+support_sep), support_height-.5] ) (
			cube( [width, support_size, .5] )
		)
	)
"""

parts.append(up(support_height)(cube([width, length, base_thickness])))

parts.append(
    translate([0, 0, support_height + base_thickness])(
        cube([width, border_size, base_thickness])
    )
)
parts.append(
    translate([0, 0, support_height + base_thickness])(
        cube([border_size, length, base_thickness])
    )
)
parts.append(
    translate([0, length - border_size, support_height + base_thickness])(
        cube([width, border_size, base_thickness])
    )
)
parts.append(
    translate([width - border_size, 0, support_height + base_thickness])(
        cube([border_size, length, base_thickness])
    )
)

scale_amt = 0.61

parts.append(
    translate(
        [border_size * 2, border_size * 2, support_height + base_thickness - 0.01]
    )(
        scale([scale_amt, scale_amt, 1])(
            dxf_linear_extrude("0131.dxf", height=base_thickness)
        )
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
