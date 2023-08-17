import copy
import math
import os
import platform
import random
from collections import deque, namedtuple
from pathlib import Path

from solid import *
from solid.utils import *
from tqdm import tqdm

from cad.common import polytri
from cad.common.helper import *

layers = []

parts = []

rows = []

random.seed(1)

for z in range(10):
    row = []
    num = random.randint(10, 20)
    rad = random.uniform(1, 3)
    for i in range(num):
        a = (i / num) * math.pi * 2
        row.append(Vec3(math.cos(a) * rad, math.sin(a) * rad, z))

    row = deque(row)

    row.rotate(random.randint(0, len(row)))

    row = list(row)

    rows.append(row)

parts.append(rings_to_polyhedron(rows))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
