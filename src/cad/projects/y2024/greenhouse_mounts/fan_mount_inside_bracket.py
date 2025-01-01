from solid import *
from solid.utils import *

from cad.projects.y2024.greenhouse_mounts.basic import (
    build_inside_part,
    full_height,
    full_width,
    metal_thickness,
)

parts = []

# Length along the metal frame
length = 45

# Stem length
stem_length = 31.5
stem_radius = 9.25 / 2
stem_washer_radius = 14

body = build_inside_part(length)

# Move the body into the printable position
body = translate([-full_width / 2, length, 0])(rotate(a=90, v=[1, 0, 0])(body))

# Raise area for washer to push against
# TODO: if the fan gets mounted on the other side, this cylinder goes a bit into an inset area in the fan body.
# Solutions:
# 1. Make the cylinder bigger such that it doesn't go into the inset
# 2. Make the cylinder taller, but then it only works for one side
# 3. Use washers to fit in the inset area
# 4. Print another little piece that fits in the inset area
body += translate([0, length / 2, full_height - 1])(
    cylinder(
        r=stem_washer_radius,
        h=stem_length - full_height + 1 - metal_thickness,
        segments=64,
    )
)

# Cut hole for stem
body -= translate([0, length / 2, -1])(
    cylinder(r=stem_radius, h=stem_length + 2, segments=32)
)

parts.append(body)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
