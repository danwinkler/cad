from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

f_size = 20
m_size = 14

parts.append(
    union()(
        difference()(
            translate([-f_size / 2.0, 0, 0])(cube([f_size, 10, 10])),
            translate([0, 5, 5])(
                rotate(90, [0, 1, 0])(cylinder(h=f_size + 2, r=3, center=True))
            ),
        ),
        translate([m_size / 2.0 + 0.5, 10, 0])(
            cube([3, 20, 10]),
            translate([0, 15, 5])(
                rotate(90, [0, 1, 0])(cylinder(h=3, r=2.5, center=True))
            ),
        ),
        translate([-m_size / 2.0 - 3 - 0.5, 10, 0])(
            cube([3, 20, 10]),
            translate([3, 15, 5])(
                rotate(90, [0, 1, 0])(cylinder(h=3, r=2.5, center=True))
            ),
        ),
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
