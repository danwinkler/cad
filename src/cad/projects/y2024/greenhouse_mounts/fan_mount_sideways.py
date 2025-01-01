from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.projects.y2024.greenhouse_mounts.basic import (
    build_inside_part,
    full_height,
    full_width,
    metal_thickness,
    profile_shape,
)

parts = []

# Length along the metal frame
length = 45

# Stem length
stem_length = 33.5
stem_radius = 9.25 / 2
stem_washer_radius = 14


y_offset = 20


def build_inside_part_raised(length=50):
    """This function creates a polyhedron that fits inside the profile shape, but doesn't extend to each edge."""

    # Round the edges a bit so it fits inside the profile using shapely

    shapely_poly = ShapelyPolygon(
        [(0, full_height + y_offset)]
        + profile_shape
        + [(full_width, full_height + y_offset)]
    )
    shapely_poly = shapely_poly.buffer(2).buffer(-4).buffer(2)

    # Move to openscad and extrude
    poly = polygon(shapely_poly.exterior.coords)
    poly = linear_extrude(length)(poly)

    return poly


body = build_inside_part_raised(length)

# Move the body into the printable position
body = translate([-full_width / 2, length, 0])(rotate(a=90, v=[1, 0, 0])(body))

# Cut hole for stem
body -= translate(
    [full_width / 2 - stem_length - 1, length / 2, full_height + y_offset / 2]
)(rotate(a=90, v=[0, 1, 0])(cylinder(r=stem_radius, h=full_width + 2, segments=32)))

# Cut stem screw access holes from other side
stem_screw_head_rad = 8

body -= translate(
    [full_width / 2 - stem_length, length / 2, full_height + y_offset / 2]
)(
    rotate(a=-90, v=[0, 1, 0])(
        cylinder(r=stem_screw_head_rad, h=full_width + 2, segments=32)
    )
)

# Cut holes for screws
screw_positions = [length * 0.2, length * 0.8]
screw_hole_rad = 3.5

for screw_position in screw_positions:
    body -= translate([0, screw_position, -1])(
        cylinder(r=screw_hole_rad, h=full_height + y_offset + 2, segments=32)
    )

parts.append(body)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
