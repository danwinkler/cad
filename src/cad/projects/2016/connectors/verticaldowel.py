from solid import *
from solid.utils import *

from cad.common.helper import *

inches_in_mm = 25.4
half_in = inches_in_mm / 2.0

floor_thickness = 5
connector_length = 30
size = half_in + 0.5
rad = size / 2
wall_thickness = 3

parts = []

wall = cylinder(r=rad + wall_thickness, h=connector_length)
hole = up(-1)(cylinder(r=rad, h=connector_length + 2))
side_hole = translate([0, -5, connector_length / 2 + 5])(
    rotate(a=90, v=[1, 0, 0])(cylinder(r=1.5, h=6, segments=12))
)

base = scale([3, 1.2, 1])(cylinder(r=rad + wall_thickness, h=floor_thickness))
base += up(floor_thickness)(
    cylinder(r1=(rad + wall_thickness) * 1.2, r2=rad + wall_thickness, h=3)
)

screw_hole = cylinder(r=1.5, h=5, segments=12) + up(3)(
    cylinder(r1=1.5, r2=3, h=2, segments=12)
)
shole1 = left(20)(screw_hole)
shole2 = right(20)(screw_hole)

part = wall
part += base
part -= hole
part -= side_hole
part -= shole1
part -= shole2

parts.append(part)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
