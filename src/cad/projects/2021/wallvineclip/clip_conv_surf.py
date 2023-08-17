import math

from lib import pyconvsurf
from lib.helper import *
from solid import cube, cylinder, rotate, scad_render, translate

parts = []

base_size = 20
base_height = 5
hook_radius = 15
hook_thickness = 7
screw_head_top_rad = 4
screw_bottom_rad = 2
screw_cone_height = 3.5


def basic_shape():
    surf = pyconvsurf.ConvSurf(margin=15, resolution=0.5)

    # Add base
    base_s = 2.2
    corner_distance = base_size * 0.5 - 3
    corners = [
        [-corner_distance, -corner_distance, 0],
        [corner_distance, -corner_distance, 0],
        [corner_distance, corner_distance, 0],
        [-corner_distance, corner_distance, 0],
    ]
    surf.add_triangle(corners[0], corners[1], corners[2], s=base_s)
    surf.add_triangle(corners[0], corners[2], corners[3], s=base_s)

    # Add hooks
    angle = 165
    angle_rads = math.radians(angle)
    num_points = 13
    angle_per_point = angle_rads / num_points
    angles = [angle_per_point * i for i in range(num_points)]

    points = [
        Vec3(
            math.sin(a) * hook_radius,
            a * 0.001,
            hook_radius - math.cos(a) * hook_radius,
        )
        for a in angles
    ]

    hook_s = 1.5
    for a, b in pairwise(points):
        surf.add_line(
            a.to_list(),
            b.to_list(),
            s=hook_s,
        )
        surf.add_line(
            (a * Vec3(-1, 1, 1)).to_list(),
            (b * Vec3(-1, 1, 1)).to_list(),
            s=hook_s,
        )

    vertices, triangles = surf.generate()
    print(f"num vertices: {len(vertices)}")
    return polyhedron(points=vertices, faces=triangles)


def screw_hole():
    segments = 24
    return hole()(
        down(1)(cylinder(r=screw_bottom_rad, h=base_height + 2, segments=segments)),
        up(base_height - screw_cone_height)(
            cylinder(
                r1=screw_bottom_rad,
                r2=screw_head_top_rad,
                h=screw_cone_height + 0.001,
                segments=segments,
            )
        ),
        up(base_height)(cylinder(r=screw_head_top_rad, h=10, segments=segments)),
    )


bottom_remove = hole()(
    translate([-base_size, -base_size, -base_size])(
        cube([base_size * 2, base_size * 2, base_size])
    )
)

parts += [basic_shape(), screw_hole(), bottom_remove]

do_rot_45 = True

if do_rot_45:
    parts = up(2.5)(
        [rotate(a=45, v=[1, 0, 0])(p) for p in parts]
    ) - translate([-30, -30, -10]) (cube([60, 60, 10]))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
