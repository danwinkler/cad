import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []
aparts = []

# front hook
parts.append(
    translate([0, -8.5, 0])(cube([40, 17, 9]))
    - translate([7, -10, 9])(rotate(v=[0, 1, 0], a=150)(down(5)(cube([20, 20, 5]))))
)

# front hook connect
parts.append(translate([25, -8.5, 9])(cube([15, 17, 9])))

# main spar
parts.append(translate([26, -13, 12])(rotate(v=[0, 1, 0], a=-3)(cube([139, 26, 8]))))

# back snap
parts.append(translate([163.5, -4.25, 0])(cube([1.5, 8.5, 63.5 / 2 - 2])))

# backsnap hook
parts.append(
    translate([163.5, -4.25, 4.5])(
        rotate(v=[1, 0, 0], a=-90)(
            linear_extrude(height=8.5)(
                polygon(points=[[0, 0], [4.5, 0], [1.5, 4.5], [0, 4.5]])
            )
        )
    )
)

# back top
aparts.append(translate([65, -8.5, 18])(cube([100, 17, 7])))

# fuselage curve
parts.append(
    translate([165, 0, -8])(
        rotate(v=[0, 1, 0], a=-85)(
            cylinder(r1=63.5 / 2.0, r2=51 / 2.0, h=140)
            - cylinder(r1=63.5 / 2.0 - 10, r2=51 / 2.0 - 10, h=140)
            - translate([-100, -50, 0])(cube([100, 100, 200]))
        )
    )
)

# parts = up( 18 ) ( rotate( v=[1,0,0], a=180 ) ( parts ) )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
