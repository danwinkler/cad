import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

parts.append(cylinder(10, 40))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
