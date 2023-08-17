import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []


def body(
    r_parts=6,
    h_parts=5,
    height=50,
    bottom=17,
    top=12,
    wall_thickness=2,
    top_inner_offset=6,
):
    dif = bottom - top

    def width_fn(r, h):
        return bottom - h * dif

    def outer_fn(h, a):
        a *= math.pi * 2
        a += h * math.pi * 2
        rad = width_fn(a, h)
        x = math.cos(a) * rad
        y = math.sin(a) * rad
        z = h * height

        return [x, y, z]

    def inner_fn(h, a):
        a *= math.pi * 2
        a += h * math.pi * 2
        rad = width_fn(a, h) - wall_thickness
        if h == 1:
            rad -= top_inner_offset
        x = math.cos(a) * rad
        y = math.sin(a) * rad
        z = h * height

        return [x, y, z]

    outer = make_trunk(h_parts, r_parts, outer_fn)
    outer -= make_trunk(h_parts, r_parts, inner_fn) - cylinder(r=1000, h=wall_thickness)

    return outer


height = 70
# parts.append( body() )
parts.append(body(height=height, bottom=20, top=15))

t_base_h = 8
t_outer_r = 19.2 / 2
t_inner_r = 13.9 / 2

le_thread = linear_extrude(height=3, center=False, convexity=10, twist=360, slices=100)(
    translate([t_outer_r, 0, 0])(sphere(r=1))
)


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def vwf(i, a):
    return 1


vine_thread = vine(
    [
        Vec3(
            math.cos(r * math.pi * 2) * t_outer_r,
            math.sin(r * math.pi * 2) * t_outer_r,
            3 * r,
        )
        for r in frange(0, 1, 0.05)
    ],
    vwf,
    8,
)

threads = up(height)(
    (cylinder(r=t_outer_r, h=t_base_h) - cylinder(r=t_inner_r, h=t_base_h))
    + up(3)(vine_thread)
)

parts.append(threads)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
