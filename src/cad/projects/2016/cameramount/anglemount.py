from solid import *
from solid.utils import *

from cad.common.helper import *

part_spacing = 0.1

# Base
part = cube([24, 24, 3])

# Vertical part
part += translate([4, 4, 3])(
    union()(
        cube([16, 16, 12]),
        translate([0, 8, 12])(
            rotate(v=[0, 1, 0], a=90)(cylinder(r=8, h=16, segments=64))
        ),
    )
    - union()(
        # slots
        translate([4 - part_spacing, 0, 3.5])(cube([4 + part_spacing * 2, 16, 25])),
        translate([12 - part_spacing, 0, 3.5])(cube([4 + part_spacing * 2, 16, 25])),
        # hole
        translate([0, 8, 12])(
            rotate(v=[0, 1, 0], a=90)(cylinder(r=2.15, h=16, segments=32))
        ),
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(part))

part += translate([-24, 0, 0])(
    cube([24, 24, 3]) - translate([12, 12, 0])(cylinder(r=6.9 / 2.0, h=3))
)

print("Saving File")
with open(__file__ + "_withhole.scad", "w") as f:
    f.write(scad_render(part))
