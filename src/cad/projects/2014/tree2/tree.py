import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []


def r_vine():
    points = []

    points.append(Vec3(0, 0, 0))

    variance = 0.3
    z_var = 0.1
    length = 4
    height = 50

    vec = Vec3(0, 0, 1)
    for i in range(height):
        vec.normalize()

        lp = points[-1]

        dx = 0
        mx = 0
        if lp.x != 0:
            dx = lp.x + 20
            mx = ((dx**2) * i**2 * 0.000001) * (-1 if dx > 0 else 1)

        dy = 0
        my = 0
        if lp.y != 0:
            dy = lp.y
            my = ((dy**2) * 0.001) * (-1 if dy > 0 else 1)

        vec.x += random.uniform(-variance, variance) + mx
        vec.y += random.uniform(-variance, variance) + my
        # vec.z += random.uniform( -z_var, z_var )
        vec.z += 0.1

        vec.normalize()

        vec *= length

        np = points[-1] + vec

        points.append(np)

    def wf(pi, r):
        return 4

    return vine(points, wf)


vines = 20
for i in range(vines):
    angle = (i / float(vines)) * 360
    parts.append(rotate(angle)(translate([20, 0, 0])(r_vine())))

parts.append(down(2)(cylinder(r=25, h=4)))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
