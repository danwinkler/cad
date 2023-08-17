import math
import random

import distmesh as dm
import matplotlib.pyplot as plt
import numpy as np

from cad.common.helper import *

lines = []

p0 = Vec3(0, 0, 0)
p1 = Vec3(1, 0, 0)
p2 = Vec3(0, 1, 0)
p3 = Vec3(0, 0, 1)

lines.append([p0, p1])
lines.append([p0, p2])
lines.append([p0, p3])


def fn(p):
    # p = p[0]
    # return math.sqrt( p[0]**2+p[1]**2+p[2]**2 )-1.0
    return np.sqrt((p**2).sum(1)) - 1.0


p, t = dm.distmeshnd(fn, dm.huniform, 0.2, (-1, -1, -1, 1, 1, 1))

dm.simpplot(p, t)
