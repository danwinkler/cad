import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

from . import lightswitch as ls

parts = []

parts.append(ls.face)

for i in range(10):
    r = random.uniform(3, 10)
    parts.append(
        translate([random.uniform(r, ls.fx - r), random.uniform(r, ls.fy - r), 0])(
            sphere(r=r)
        )
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
