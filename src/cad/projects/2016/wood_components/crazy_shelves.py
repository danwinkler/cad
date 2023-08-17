import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

top_left = Vec3(0, 1000)
top_right = Vec3(1000, 1000)

left_shelf_top = top_left.copy()
left_shelf_base = Vec3(-50 + random.random() * 100, 0)
left_shelf_vec = left_shelf_top - left_shelf_base

right_shelf_top = top_right.copy()
right_shelf_base = Vec3(950 + random.random() * 100, 0)
right_shelf_vec = right_shelf_top - right_shelf_base

parts.append(
    translate(left_shelf_base.to_list())(
        rot_on_vec(
            Vec3(left_shelf_vec.x, 0, left_shelf_vec.y),
            cube([20, 300, left_shelf_vec.length()]),
        )
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
