import math
import random
import functools
from dataclasses import dataclass

from solid import *
from solid.utils import *

from lib.helper import *

parts = []

base_size = 20
base_height = 5
hook_radius = 15
hook_thickness = 7
screw_head_top_rad = 4
screw_bottom_rad = 2
screw_cone_height = 3.5


def base():
    segments = 24
    corner_distance = base_size * 0.5 - base_height
    corners = [
        translate([-corner_distance, -corner_distance, 0])(
            sphere(r=base_height, segments=segments)
        ),
        translate([corner_distance, -corner_distance, 0])(
            sphere(r=base_height, segments=segments)
        ),
        translate([corner_distance, corner_distance, 0])(
            sphere(r=base_height, segments=segments)
        ),
        translate([-corner_distance, corner_distance, 0])(
            sphere(r=base_height, segments=segments)
        ),
    ]

    return hull()(corners)


def hook():
    # segments = 24
    # angle = 280

    # def cap(a):
    #     return rotate(a, [0, 0, 1])(
    #         translate([hook_radius, 0, 0])(
    #             rotate(90, [1, 0, 0])(sphere(r=hook_thickness * 0.5, segments=segments))
    #         )
    #     )

    # rot_angle = angle + 90 + (360 - angle) * 0.5
    # ring_shape = rotate(a=-rot_angle, v=[0, 0, 1])(
    #     rotate_extrude(angle=angle, segments=segments * 2)(
    #         translate([-hook_radius, 0])(
    #             circle(r=hook_thickness * 0.5, segments=segments)
    #         )
    #     )
    #     + cap(angle + 180)
    #     + cap(180)
    # )

    # ring = translate([0, 0, hook_radius])(rotate(90, [1, 0, 0])(ring_shape))

    angle = 160
    angle_rads = math.radians(angle)

    def cap(a):
        return rotate(a, [0, 0, 1])(
            translate([hook_radius, 0, 0])(
                rotate(90, [1, 0, 0])(sphere(r=hook_thickness * 0.5, segments=24))
            )
        )

    def side():
        num_points = 128
        angle_per_point = angle_rads / num_points
        total_distance = angle_rads * hook_radius
        curved_tip_start = math.ceil(
            num_points - (hook_thickness / total_distance) * num_points
        )
        angles = [angle_per_point * i for i in range(num_points)]

        points = [
            Vec3(math.sin(a) * hook_radius, 0, hook_radius - math.cos(a) * hook_radius)
            for a in angles
        ]

        def angle_dist_from_zero(a):
            a = a % (2 * math.pi)
            return min(abs(a), abs(a - math.pi), abs(a - math.pi * 2))

        def wf(index, a):
            max_base_width = 7
            fat_base_start_index = num_points // 6.5
            # if index < fat_base_start_index:
            #     fat_base = 1
            # else:
            fat_base = (
                min((25 / (abs(index - fat_base_start_index) + 5)), 2)
                * 2
                * (-math.cos(2 * a) + 1)
                * 0.5
                # * angle_dist_from_zero(a)
                # * (abs(math.sin(a) + 0.1))
            )

            if index < curved_tip_start:
                curved_tip = 1
            elif index == num_points - 1:
                curved_tip = 0
            else:
                total_curve_points = num_points - curved_tip_start
                current_curve_index = (total_curve_points - (num_points - index)) + 1
                curve_angle = min(
                    (current_curve_index / total_curve_points) * math.pi * 0.5, 1
                )
                print(curve_angle)
                curved_tip = math.sin(math.acos(curve_angle))

            return min(hook_thickness * 0.5 + fat_base, max_base_width) * curved_tip

        return vine(points, wf, sections=32)

    # rot_angle = angle * 2 + 90 + (360 - angle * 2) * 0.5
    # caps = translate([0, 0, hook_radius])(
    #     rotate(90, [1, 0, 0])(
    #         rotate(a=-rot_angle, v=[0, 0, 1])(cap(angle * 2 + 180) + cap(180))
    #     )
    # )

    return side() + scale([-1, 1, 1])(side())


def screw_hole():
    segments = 24
    return hole()(
        down(1)(cylinder(r=screw_bottom_rad, h=base_height + 2, segments=segments)),
        up(base_height - screw_cone_height)(
            cylinder(
                r1=screw_bottom_rad,
                r2=screw_head_top_rad,
                h=screw_cone_height,
                segments=segments,
            )
        ),
        up(base_height)(cylinder(r=screw_head_top_rad, h=10, segments=segments)),
    )


bottom_remove = hole()(
    translate([-base_size, -base_size, -base_height])(
        cube([base_size * 2, base_size * 2, base_height])
    )
)

parts += [base(), hook(), screw_hole(), bottom_remove]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
