import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

point_count = 50
distance = math.pi * 8
points = [
    Vec3(math.cos(a) * 3, math.sin(a) * 3, a)
    for a in [(i / float(point_count - 1)) * distance for i in range(point_count)]
]

parts.append(vine(points, lambda h, a: 1, sections=6))

parts.append(vine([Vec3(i, 0, 0) for i in range(10)], lambda h, a: 1, sections=6))
parts.append(vine([Vec3(0, i, 0) for i in range(10)], lambda h, a: 1, sections=6))
parts.append(vine([Vec3(0, 0, i) for i in range(10)], lambda h, a: 1, sections=6))


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
