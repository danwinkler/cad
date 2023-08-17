from solid import *
from solid.utils import *

parts = []

holes = []


def inset():
    return down(15)(
        union()(
            rotate(-45, [0, 0, 1])(
                translate([0, 7, 10])(rotate(-90, [1, 0, 0])(cylinder(r1=4, r2=0, h=3)))
            ),
            (
                cylinder(h=30, r=8.5, center=True)
                * translate([0.5, 0.5, -50])(cube([100, 100, 100]))
            )
            - cylinder(h=31, r=6, center=True),
        )
    )


parts.append(
    difference()(
        cylinder(h=30, r=10, center=True) - cylinder(h=31, r=8, center=True),
        inset(),
        rotate(180, [0, 0, 1])(inset()),
    )
)


def grabber():
    return up(15)(
        union()(
            rotate(-45, [0, 0, 1])(
                translate([0, 6.5, 10])(
                    rotate(-90, [1, 0, 0])(cylinder(r1=4, r2=0, h=3))
                )
            ),
            (
                cylinder(h=30, r=8, center=True)
                * translate([1, 1, -50])(cube([100, 100, 100]))
            ),
        )
        - cylinder(h=31, r=6, center=True)
    )


parts.append(grabber())
parts.append(rotate(180, [0, 0, 1])(grabber()))

holes.append(up(4.9)(cylinder(r1=8, r2=0, h=10, center=True)))

with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts) - union()(holes)))
