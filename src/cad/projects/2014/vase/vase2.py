import math
import random

from solid import *
from solid.utils import *

parts = []

h_sections = 20
v_sections = 30

height_scalar = 2

lines = []


def rad_f(y):
    global v_sections
    return math.sin((float(y) / v_sections) * math.pi * 2) * 10 + 20


print("Building Line Segments")
for r in range(h_sections):
    line = []
    a = math.pi * 2 * (float(r) / h_sections)
    da = 0.1
    for y in range(v_sections):
        # da += random.uniform( -.01, .01 )
        a += da
        if da > 0.15 or da < -0.15:
            da *= -0.9
        rad = rad_f(y)
        line.append([math.cos(a) * rad, math.sin(a) * rad, y * height_scalar])
    lines.append(line)

for r in range(h_sections):
    line = []
    a = math.pi * 2 * (float(r) / h_sections)
    da = -0.1
    for y in range(v_sections):
        # da += random.uniform( -.01, .01 )
        a += da
        if da > 0.15 or da < -0.15:
            da *= -0.9
        rad = rad_f(y)
        line.append([math.cos(a) * rad, math.sin(a) * rad, y * height_scalar])
    lines.append(line)


print("Hull And unioning Lines")
for line in lines:
    sp = []
    i = 0
    while i < len(line) - 1:
        sp.append(
            hull()(translate(line[i])(sphere(1)), translate(line[i + 1])(sphere(1)))
        )
        i += 1
    parts.append(union()(sp))

parts.append(down(1)(cylinder(h=2, r=21)))

parts.append(
    up(height_scalar * (v_sections - 1))(
        minkowski()(cylinder(h=1, r=19), sphere(0.5)) - down(0.5)(cylinder(h=3, r=17))
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
