import math

from solid import *
from solid.utils import *

from cad.common import *
from cad.common import pyconvsurf

parts = []

width = 50
hook_radius = 30


def basic_shape():
    surf = pyconvsurf.ConvSurf(margin=15, resolution=1)

    # Add hooks
    angle = 135
    angle_rads = math.radians(angle)
    num_points = 13
    angle_per_point = angle_rads / num_points
    angles = [angle_per_point * i for i in range(num_points)]

    points = [
        Vec3(
            0,
            (-math.sin(a) * hook_radius) * 1.4,
            hook_radius - math.cos(a) * hook_radius,
        )
        for a in angles
    ]

    def cp(p, x=None, y=None, z=None):
        return Vec3(
            x if x is not None else p.x,
            y if y is not None else p.y,
            z if z is not None else p.z,
        )

    hook_s = 2
    for i, p in enumerate(points[:-1]):
        p0 = cp(p, x=-width * 0.5)
        p1 = cp(points[i + 1], x=-width * 0.5)
        p2 = cp(p, x=width * 0.5)
        p3 = cp(points[i + 1], x=width * 0.5)
        surf.add_triangle(p0, p2, p3, s=hook_s)
        surf.add_triangle(p0, p1, p3, s=hook_s)

    max_z = max(p.z for p in points)

    # Add back
    surf.add_rect(
        [-width * 0.5, 0, 0],
        [width * 0.5, 0, 0],
        [width * 0.5, 0, max_z],
        [-width * 0.5, 0, max_z],
    )

    vertices, triangles = surf.generate()
    print(f"num vertices: {len(vertices)}")
    return polyhedron(points=vertices, faces=triangles)


bottom_remove = hole()(
    translate([-width * 2, -width * 2, -width * 2])(
        cube([width * 4, width * 4, width * 2])
    )
)

back_remove = hole()(
    translate([-width * 2, 0, -width * 2])(cube([width * 4, width * 2, width * 4]))
)

hole_z = 30
first_hole_rad = 10
screw_head_top_rad = 4
screw_bottom_rad = 2
screw_cone_height = 3.5
hole_remove = hole()(
    translate([0, -60, hole_z])(
        rotate(a=-90, v=[1, 0, 0])(cylinder(r=first_hole_rad, h=30, segments=24))
    ),
    translate([0, 0, hole_z])(
        rotate(a=90, v=[1, 0, 0])(
            cylinder(r=screw_bottom_rad, h=10, segments=24),
            up(3)(
                cylinder(
                    r1=screw_bottom_rad,
                    r2=screw_head_top_rad,
                    h=screw_cone_height,
                    segments=24,
                )
            ),
        )
    ),
)

parts += [basic_shape(), bottom_remove, back_remove, hole_remove]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
