import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

mm_in_inch = 25.4

scale_ratio = 209.0 / 196.0

plate = scale([1, scale_ratio, 1])(
    translate([-8.5 * 0.5 * mm_in_inch, -11 * 0.5 * mm_in_inch, 0])(
        linear_extrude(height=3)(import_dxf("pickguard2.dxf"))
    )
)


parts = plate
p1 = plate - translate([-1000, 0, -1])(cube([2000, 1000, 5]))
p2 = plate - translate([-1000, -1000, -1])(cube([2000, 1000, 5]))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

with open(__file__ + "_p1.scad", "w") as f:
    f.write(scad_render(union()(p1)))

with open(__file__ + "_p2.scad", "w") as f:
    f.write(scad_render(union()(p2)))
