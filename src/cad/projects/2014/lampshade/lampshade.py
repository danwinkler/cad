import math
import random

from solid import *
from solid.utils import *

parts = []

h_sections = 80
v_sections = 20
hole_rad = 21
wall_thickness = 1.5
v_scale = 4
debug = False


def r(a, z):
    ret = hole_rad + wall_thickness  # Space for the inner hole
    ret += 30 - (1.0 / ((z * 0.3) + 1)) * 30  # The little curve next to the hole
    ret += (1.0 / ((v_sections - z) + 2)) * 30  # curve at the base
    if z >= 1:
        ret += math.sin(a * 12) * 1.5
        ret += math.cos(z * 0.25 * v_scale) * 1.5
    return ret


rings = []

for z in range(v_sections):
    points = []
    for i in range(h_sections):
        angle = (math.pi * 2) / h_sections * i
        point = [
            math.sin(angle) * r(angle, z),
            math.cos(angle) * r(angle, z),
            z * v_scale,
        ]
        if z == 0:
            point[2] = v_scale
        points.append(point)
    rings.append(points)

for z in range(v_sections - 1):
    for i in range(h_sections):
        if debug:
            parts.append(translate(rings[z][i])(sphere(wall_thickness)))
        else:
            parts.append(
                hull()(
                    translate(rings[z][i])(sphere(wall_thickness)),
                    translate(rings[z][(i + 1) % h_sections])(sphere(wall_thickness)),
                    translate(rings[z + 1][i])(sphere(wall_thickness)),
                    translate(rings[z + 1][(i + 1) % h_sections])(
                        sphere(wall_thickness)
                    ),
                )
            )

# parts.append( cylinder( h=3, r=32 ) - down( 1 ) ( cylinder( h=5, r=21 ) ) )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
