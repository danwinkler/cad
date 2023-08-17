import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

# Small desktop water fountain
# Ordered small water pump from amazon
# Rotating part at top of fountain that, when spins, alternates blocking some of the holes for the water to spray out of
# So that you get like an alternating patten of water spraying out of the top

diameter = 7.85

parts = []


parts.append(cylinder(6, 10) - cylinder(4, 10))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
