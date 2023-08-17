import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

stem_rad = 5

hole_depth = 10
hole_size = 2.5

parts.append(cylinder(r=stem_rad, h=40) + cylinder(r=hole_size, h=48, segments=36))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
