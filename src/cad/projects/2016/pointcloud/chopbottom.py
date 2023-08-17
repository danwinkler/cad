import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

parts.append(
    import_stl(file="structure.stl")
    - translate([-1000, -1000, -1000])(cube([2000, 2000, 1000]))
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
