import math
import random
import sys

from solid import *
from solid.utils import *

from cad.common.helper import make_trunk

parts = []

parts.append(cylinder(r=30, h=3))


def leg1(h, s):
    r = s * math.pi * 2 + h
    x = math.sin(h * 5) * 5
    y = h * 20 + h**6 * 13
    scale = (1 - h) * 2 + 1
    xscale = 1

    yscale = 1
    if s < 0.01:
        scale += 3
    elif s - 1.0 / 3 < 0.001:
        yscale = 2
        xscale = 2
    elif s - 2.0 / 3 < 0.001:
        scale = 0.5

    return [x + math.cos(r) * scale * xscale, math.sin(r) * scale * yscale + y, h * 50]


for i in range(12):
    a = i / 12.0 * 360
    parts.append(
        up(3)(
            rotate(a, [0, 0, 1])(
                right(-28)(
                    union()(
                        rotate(-360 / 12, [0, 0, 1])(make_trunk(20, 3, leg1)),
                        rotate(360 / 12, [0, 0, 1])(
                            mirror([0, 1, 0])(make_trunk(20, 3, leg1))
                        ),
                    )
                )
            )
        )
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
