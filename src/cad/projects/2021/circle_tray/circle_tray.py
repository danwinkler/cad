from solid import *
from solid.utils import *

from cad.common.helper import *

diameter = 241
rad = diameter / 2

bottom_thickness = 5
wall_height = 20
wall_thickness = 2
segments = 64


def bottom():
    cyl = cylinder(r=rad, h=bottom_thickness, segments=segments)
    bottom_ridges = hole()(
        [
            translate([x, -rad, 0])(
                rotate(a=-90, v=[1, 0, 0])(cylinder(r=3, h=diameter))
            )
            for x in range(-int(rad) + 10, int(rad), 10)
        ]
    )
    top_ridges = [
        translate([x - 5, -rad, 5])(
            rotate(a=-90, v=[1, 0, 0])(cylinder(r=3, h=diameter))
        )
        for x in range(-int(rad), int(rad) + 10, 10)
    ]

    top_ridges = union()(top_ridges) - (
        cylinder(r=diameter, h=20, segments=segments)
        - cylinder(r=rad - 1, h=20, segments=segments)
    )

    return cyl + bottom_ridges + top_ridges


def walls():
    return cylinder(r=rad, h=wall_height, segments=segments) - down(1)(
        cylinder(r=rad - wall_thickness, h=wall_height + 2, segments=segments)
    )


parts = []

parts.append(bottom())
parts.append(walls())


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
