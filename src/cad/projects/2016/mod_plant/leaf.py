import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

w2 = 21
w3 = 19

h0 = 5
h2 = 21
h3 = 54
h4 = 80

thickness = 5
stem_rad = 5

hole_depth = 10
hole_size = 2.5 + 0.2  # extra so that the 2.5 rad connector can fit

outline = polygon(points=[[0, h0], [w2, h2], [w3, h3], [0, h4], [-w3, h3], [-w2, h2]])

parts.append(
    (
        translate([0, thickness / 2.0, 0])(
            rotate(v=[1, 0, 0], a=90)(linear_extrude(height=5)(outline))
        )
        + cylinder(r1=stem_rad, r2=1, h=h4 - 2)
    )
    - cylinder(r=hole_size, h=hole_depth, segments=36)
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
