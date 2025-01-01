import math

from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *

# The profile of the metal kind of looks like this:
# Top side
#    |
#   ----     ----
#       \___/ - angle side
#         |
#     Bottom side

metal_thickness = 1.2

full_width = 59.5
full_height = 21
bottom_side = 14.75
top_side = 11.5

bottom_side_x_offset = full_width / 2 - bottom_side / 2

profile_shape = [
    (0, full_height),
    (top_side, full_height),
    (bottom_side_x_offset, 0),
    (bottom_side_x_offset + bottom_side, 0),
    (full_width - top_side, full_height),
    (full_width, full_height),
]


def build_inside_part(length=50):
    """This function creates a polyhedron that fits inside the profile shape, but doesn't extend to each edge."""

    # Round the edges a bit so it fits inside the profile using shapely
    shapely_poly = ShapelyPolygon(profile_shape[1:-1])
    shapely_poly = shapely_poly.buffer(-2).buffer(2)

    # Move to openscad and extrude
    poly = polygon(shapely_poly.exterior.coords)
    poly = linear_extrude(length)(poly)

    return poly


def build_outside_part(length=50, outside_width=full_width - 20, offset_distance=15):
    """This function creates a polyhedron that fits outside the profile shape."""

    # Reduce the height a bit to make room for the metal size
    height_offset = -2

    # Start with a rectangle that is the full size of the profile
    shapely_poly = ShapelyPolygon(
        [
            (0, full_height + height_offset),
            (full_width, full_height + height_offset),
            (full_width / 2 + outside_width / 2, -offset_distance),
            (full_width / 2 - outside_width / 2, -offset_distance),
        ]
    )

    # Subtract the inside shape, buffered out
    buffer_amount = 2
    shapely_inside_shape = ShapelyPolygon(profile_shape[1:-1])
    shapely_inside_shape = shapely_inside_shape.buffer(buffer_amount)
    shapely_poly = shapely_poly.difference(shapely_inside_shape)

    if hasattr(shapely_poly, "geoms"):
        print(
            "Warning: shapely_poly is a multi-polygon, but should only have one element"
        )
        shapely_poly = shapely_poly.geoms[0]

    shapely_poly = shapely_poly.buffer(-1).buffer(1)

    # Move to openscad and extrude
    poly = polygon(shapely_poly.exterior.coords)
    poly = linear_extrude(length)(poly)

    return poly


if __name__ == "__main__":
    parts = []

    # parts.append(build_inside_part())
    parts.append(build_outside_part(length=5))

    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(scad_render(union()(parts)))
