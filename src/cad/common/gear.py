"""
From https://github.com/marmakoide/gear-profile-generator
"""

import numpy as np
from shapely.affinity import rotate, scale, translate
from shapely.geometry import MultiPoint, Point, Polygon, box
from shapely.ops import unary_union


def rot_matrix(x):
    c, s = np.cos(x), np.sin(x)
    return np.array([[c, -s], [s, c]])


def rotation(X, angle, center=None):
    if center is None:
        return np.dot(X, rot_matrix(angle))
    else:
        return np.dot(X - center, rot_matrix(angle)) + center


def deg2rad(x):
    return (np.pi / 180) * x


def generate(
    teeth_count=8,
    tooth_width=1.0,
    pressure_angle=deg2rad(20.0),
    backlash=0.0,
    frame_count=16,
):
    tooth_width -= backlash
    pitch_circumference = tooth_width * 2 * teeth_count
    pitch_radius = pitch_circumference / (2 * np.pi)
    addendum = tooth_width * (2 / np.pi)
    dedendum = addendum
    outer_radius = pitch_radius + addendum
    # Tooth profile
    profile = np.array(
        [
            [-(0.5 * tooth_width + addendum * np.tan(pressure_angle)), addendum],
            [-(0.5 * tooth_width - dedendum * np.tan(pressure_angle)), -dedendum],
            [(0.5 * tooth_width - dedendum * np.tan(pressure_angle)), -dedendum],
            [(0.5 * tooth_width + addendum * np.tan(pressure_angle)), addendum],
        ]
    )

    outer_circle = Point(0.0, 0.0).buffer(outer_radius)

    poly_list = []
    prev_X = None
    l = 2 * tooth_width / pitch_radius
    for theta in np.linspace(0, l, frame_count):
        X = rotation(profile + np.array((-theta * pitch_radius, pitch_radius)), theta)
        if prev_X is not None:
            poly_list.append(
                MultiPoint([x for x in X] + [x for x in prev_X]).convex_hull
            )
        prev_X = X

    def circle_sector(angle, r):
        box_a = rotate(box(0.0, -2 * r, 2 * r, 2 * r), -angle / 2, Point(0.0, 0.0))
        box_b = rotate(box(-2 * r, -2 * r, 0, 2 * r), angle / 2, Point(0.0, 0.0))
        return Point(0.0, 0.0).buffer(r).difference(box_a.union(box_b))

    # Generate a tooth profile
    tooth_poly = unary_union(poly_list)
    tooth_poly = tooth_poly.union(scale(tooth_poly, -1, 1, 1, Point(0.0, 0.0)))

    # Generate the full gear
    gear_poly = Point(0.0, 0.0).buffer(outer_radius)
    for i in range(0, teeth_count):
        gear_poly = rotate(
            gear_poly.difference(tooth_poly),
            (2 * np.pi) / teeth_count,
            Point(0.0, 0.0),
            use_radians=True,
        )

    # Job done
    return gear_poly, pitch_radius
