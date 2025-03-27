import math

from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *

in_to_mm = 25.4


def chord_length(r, angle_deg):
    """
    Returns the chord length for a circle of radius r
    subtending 'angle_deg' degrees at the center.
    Formula: L = 2 * r * sin(angle/2).
    """
    angle_rad = math.radians(angle_deg)
    return 2 * r * math.sin(angle_rad / 2)


def build_cover():
    parts = []

    wood_thickness = 1.5 * in_to_mm
    wood_width = 3 * in_to_mm
    arc_radius = 16.5 * in_to_mm
    wood_placement_radius = arc_radius + 0.5 * in_to_mm

    # Create a cylinder to represent arc
    arc = color([0.4, 0.3, 0.9])(down(10)(cylinder(r=arc_radius, h=10, segments=120)))

    parts.append(arc)

    def make_segment():
        length = chord_length(wood_placement_radius, 15)

        print(f"Length: {length/25.4} inches")
        segment = cube([length, wood_width, wood_thickness])

        # Cut each end at an angle
        segment -= translate([0, 0, 0])(
            rotate(a=-7.5, v=[0, 0, 1])(
                translate([-20, -1, -1])(cube([20, wood_width + 2, wood_thickness + 2]))
            )
        )

        segment -= translate([length, 0, 0])(
            rotate(a=7.5, v=[0, 0, 1])(
                translate([0, -1, -1])(cube([20, wood_width + 2, wood_thickness + 2]))
            )
        )

        return segment

    for i in range(0, 90, 15):
        a = math.radians(i)
        parts.append(
            translate(
                [
                    math.cos(a) * wood_placement_radius,
                    math.sin(a) * wood_placement_radius,
                    0,
                ]
            )(rotate(a=i + 90 + 7.5, v=[0, 0, 1])(make_segment()))
        )

    return parts


parts = []

parts.append(build_cover())

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
