import math
import random
import sys

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

cup_radius = 35.7  # The radius from the center of the cup to the edge of the rim
cup_thickness = 4  # The thickness of the cup at the rim
acorn_holder_size = 15  # How large the holder for the acorn should be
rim_height = 10  # How far down past the rim the top should go
bowl_depth = 40  # How deep into the cup the top should go
num_holes = 6
segments = 60
thickness = 3  # The wall thickness of the top
t2 = thickness / 2  # thickness / 2

rim_test = False  # If true, only prints out rim


profile_shapes = [
    # Bottom edge of outer rim
    translate([cup_radius + t2, rim_height])(sphere(r=t2, segments=16)),
    # Top outer edge of rim
    translate([cup_radius + t2, t2])(sphere(r=t2, segments=16)),
    # Inner edge of rim
    translate([cup_radius - cup_thickness - t2, t2])(sphere(r=t2, segments=16)),
    # Connection to center acorn holder
    translate([acorn_holder_size / 2 + t2, bowl_depth + 2])(sphere(r=t2, segments=16)),
]

if rim_test:
    profile_shapes = profile_shapes[:3]

profile = None
for a, b in zip(profile_shapes, profile_shapes[1:]):
    combined = hull()(a, b)
    if profile:
        profile = profile + combined
    else:
        profile = combined

profile = projection()(profile)

rim = rotate_extrude(segments=segments)(profile)

holder = up(bowl_depth)(
    (
        sphere(r=acorn_holder_size / 2 + thickness, segments=segments)
        + hole()(sphere(r=acorn_holder_size / 2, segments=segments))
    )
    - down(acorn_holder_size * 0.8)(sphere(r=acorn_holder_size, segments=segments))
)

if rim_test:
    holder = []

holes = [
    rotate(a=360 / num_holes * i, v=[0, 0, 1])(
        translate([acorn_holder_size * 0.6, 0, 0])(
            hull()(
                cylinder(r=thickness, h=100, segments=16),
                right(cup_radius - acorn_holder_size - 10)(
                    cylinder(r=thickness, h=100, segments=16),
                ),
            )
        )
    )
    for i in range(num_holes)
]

parts.append((rim + holder) - holes)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
