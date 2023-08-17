import math

import numpy as np
import pyclipper
from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []


def shape_func(a):
    return Vec3(a * 1000, -math.sin(a * 7) * 100, 0.00000001).rotate(
        Vec3(0, 0, 1), -0.8
    )


def get_normal(a):
    v1 = a - 0.0001
    v2 = a + 0.0001
    p1 = shape_func(v1)
    p2 = shape_func(v2)
    return (p2 - p1).cross(Vec3(0, 0, 1)).normalize()


def offset(points, offset_amount, path_type=pyclipper.JT_ROUND, scale_value=100.0):
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        pyclipper.scale_to_clipper(points, scale_value),
        path_type,
        pyclipper.ET_CLOSEDPOLYGON,
    )
    return pyclipper.scale_from_clipper(
        pco.Execute(pyclipper.scale_to_clipper(offset_amount, scale_value)), scale_value
    )


def shrink_and_enlarge(points, shrink_amount, enlarge_amount, scale_value=100.0):
    shrunk_points = offset(
        points, -shrink_amount, path_type=pyclipper.JT_SQUARE, scale_value=scale_value
    )
    if len(shrunk_points) != 1:
        raise Exception(f"Failed to shrink into a single shape {len(shrunk_points)}")
    enlarged_points = offset(shrunk_points[0], enlarge_amount, scale_value=scale_value)
    if len(enlarged_points) != 1:
        raise Exception(f"Failed to enlarge into a single shape {len(shrunk_points)}")
    return enlarged_points[0]


def holder(a, an, b, bn):
    depth = 80
    wall_thickness = 2.0

    an = an.copy()
    bn = bn.copy()
    scale = 75
    an *= scale
    bn *= scale
    p0 = a - an
    p1 = a + an
    p2 = b + bn
    p3 = b - bn
    points = [p for p in [p0, p1, p2, p3]]

    top = max(points, key=lambda p: p[1])
    bottom = min(points, key=lambda p: p[1])
    average = (top + bottom) * 0.5

    points_as_lists = [p.to_list() for p in points]

    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        pyclipper.scale_to_clipper(points_as_lists),
        pyclipper.JT_SQUARE,
        pyclipper.ET_CLOSEDPOLYGON,
    )

    shrunk_points = pyclipper.scale_from_clipper(
        pco.Execute(pyclipper.scale_to_clipper(-wall_thickness))
    )[0]

    outer = linear_extrude(height=depth)(polygon(points_as_lists))
    inner = up(wall_thickness)(linear_extrude(height=depth + 1)(polygon(shrunk_points)))

    # front_panel_type = "half_cut"
    # front_panel_type = "hole"
    # front_panel_type = "shrunk_face_hole"
    # front_panel_type = "shrunk_face_half_cut"
    front_panel_type = "shrunk_hole_right_side"

    if front_panel_type == "half_cut":
        front_lip = intersection()(
            inner,
            translate([average.x - 200, average.y - 200, depth - wall_thickness])(
                cube([400, 200, wall_thickness])
            ),
        )
    elif front_panel_type == "hole":
        front_lip = intersection()(
            inner,
            translate([average.x - 200, average.y - 200, depth - wall_thickness])(
                cube([400, 400, wall_thickness])
            ),
        ) - translate([average.x, average.y, 0])(cylinder(r=20, h=depth + 1))
    elif front_panel_type == "shrunk_face_hole":
        hole_points = shrink_and_enlarge(
            points_as_lists, shrink_amount=40, enlarge_amount=15
        )

        if len(hole_points) > 1000:
            raise Exception(f"Too many points in hole {len(hole_points)}")

        shrunk_face_hole = linear_extrude(height=depth + 1)(polygon(hole_points))

        front_lip = (
            intersection()(
                inner,
                translate([average.x - 200, average.y - 200, depth - wall_thickness])(
                    cube([400, 400, wall_thickness])
                ),
            )
            - shrunk_face_hole
        )
    elif front_panel_type == "shrunk_face_half_cut":
        shrunk_points = offset(points_as_lists, -30)[0]
        shapely_shape = ShapelyPolygon(shrunk_points)
        shapely_subtract = ShapelyPolygon(
            (
                (average.x - 200, average.y - 200),
                (average.x + 200, average.y - 200),
                (average.x + 200, average.y),
                (average.x - 200, average.y),
            )
        )

        shapely_final = shapely_shape.difference(shapely_subtract)

        hole_points = offset(shapely_final.exterior.coords, 10)[0]

        if len(hole_points) > 1000:
            raise Exception(f"Too many points in hole {len(hole_points)}")

        shrunk_face_hole = linear_extrude(height=depth + 1)(polygon(hole_points))

        front_lip = (
            intersection()(
                inner,
                translate([average.x - 200, average.y - 200, depth - wall_thickness])(
                    cube([400, 400, wall_thickness])
                ),
            )
            - shrunk_face_hole
        )
    elif front_panel_type == "shrunk_hole_right_side":
        left_side_scale = 0.5
        rp0 = a - an
        rp1 = a + (an * left_side_scale)
        rp2 = b + (bn * left_side_scale)
        rp3 = b - bn
        rpoints = [p for p in [rp0, rp1, rp2, rp3]]

        shrunk_points = offset([p.to_list() for p in rpoints], -30)[0]

        shapely_shape = ShapelyPolygon(shrunk_points)
        shapely_subtract = ShapelyPolygon(
            (
                (average.x - 200, average.y - 200),
                (average.x + 200, average.y - 200),
                (average.x + 200, average.y),
                (average.x - 200, average.y),
            )
        )

        shapely_final = shapely_shape.difference(shapely_subtract)

        hole_points = offset(shapely_final.exterior.coords, 10)[0]

        shrunk_face_hole = linear_extrude(height=depth + 1)(polygon(hole_points))

        front_lip = (
            intersection()(
                inner,
                translate([average.x - 200, average.y - 200, depth - wall_thickness])(
                    cube([400, 400, wall_thickness])
                ),
            )
            - shrunk_face_hole
        )

    return (outer - inner) + front_lip


points = [(shape_func(a), get_normal(a)) for a in np.linspace(0, 1, num=12)]

for i in range(len(points) - 1):
    p1, n1 = points[i]
    p2, n2 = points[i + 1]
    parts.append(holder(p1, n1, p2, n2))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
