import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []


@in_inches
def mount():
    floor = cube([1.48, 1, 0.1])

    walls = cube([0.24, 1, 0.5]) + right(1.24)(cube([0.24, 1, 0.5]))

    return floor + walls


parts += [mount()]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
