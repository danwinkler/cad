import math

from solid import *
from solid.utils import *

from lib.helper import *

# from lib import pyconvsurf

epsilon = 0.01

# width is the total width when looking at it when mounted on a wall.
# Part is printed on it's side, so width is on the z axis.
width = 10
n_wires = 1
wire_rad = 8.0 / 2
# Distance between each wire
wire_spacing = 2
wire_y_offset = 2

wire_holder_thickness = 10

# Length of the tab on each end for holding the screw
hold_down_length = 10  # X axis
hold_down_thickness = 4  # Y axis

tab_radius = 1.7
tab_depth = 2
tab_edge_offset = 1

tab_hole_size_y = (wire_holder_thickness - hold_down_thickness) - tab_edge_offset * 2

# Screw sections
# A: small section for screw
# B: tapered section
# C: large section for head of screw
a_rad = 2
a_length = 4
b_length = 3.5
c_rad = 4
c_length = 2
segments = 24

cover_overhang_z = 3
cover_overhang_x = 3
cover_width = width + cover_overhang_z * 2
cover_thickness = 5

parts = []


def screw_head():
    return union()(
        down(epsilon)(cylinder(r=a_rad, h=a_length + epsilon * 2, segments=segments)),
        up(a_length)(
            cylinder(r1=a_rad, r2=c_rad, h=b_length + epsilon, segments=segments)
        ),
        up(a_length + b_length)(
            cylinder(r=c_rad, h=c_length + epsilon, segments=segments)
        ),
    )


midsection_length = n_wires * (wire_spacing + wire_rad * 2) + wire_spacing


def bottom_part():
    def holddown():
        screwhole = translate([hold_down_length * 0.5, 0, width * 0.5])(
            rotate(a=-90, v=[1, 0, 0])(
                down(a_length + (b_length - hold_down_thickness))(screw_head())
            )
        )
        return cube([hold_down_length, hold_down_thickness, width]) - screwhole

    def midsection():
        # Holes for wires
        holes = [
            translate(
                [
                    wire_spacing + wire_rad + i * (wire_spacing + wire_rad * 2),
                    wire_holder_thickness * 0.5 - wire_y_offset,
                    -1,
                ]
            )(cylinder(r=wire_rad, h=width + 2, segments=segments))
            for i in range(n_wires)
        ]

        # View holes
        holes += [
            translate(
                [
                    wire_spacing + wire_rad + i * (wire_spacing + wire_rad * 2),
                    wire_rad,
                    width * 0.5,
                ]
            )(
                rotate(a=-90, v=[1, 0, 0])(
                    cylinder(
                        r=wire_rad * 0.8,
                        h=wire_holder_thickness + 2,
                        segments=segments,
                    )
                )
            )
            for i in range(n_wires)
        ]

        def inset():
            mink_depth = 0.001
            return minkowski()(
                translate([mink_depth, tab_radius, tab_radius])(
                    cube(
                        [
                            tab_depth - mink_depth * 2,
                            tab_hole_size_y - tab_radius * 2,
                            width - tab_edge_offset * 2 - tab_radius * 2,
                        ]
                    )
                ),
                rotate(a=90, v=[0, 1, 0])(
                    cylinder(r=tab_radius, h=mink_depth, segments=12)
                ),
            )

        # Tab holes
        holes += [
            translate([-0.01, hold_down_thickness + tab_edge_offset, tab_edge_offset])(
                inset()
            ),
            translate(
                [
                    midsection_length - tab_depth + epsilon,
                    hold_down_thickness + tab_edge_offset,
                    tab_edge_offset,
                ]
            )(inset()),
        ]
        return cube([midsection_length, wire_holder_thickness, width]) - union()(holes)

    return union()(
        holddown(),
        translate([hold_down_length, 0, 0])(midsection()),
        translate([midsection_length + hold_down_length, 0, 0])(holddown()),
    )


def cap():
    grabber_tab_spacing = 0.35

    def grabber_piece(flip_x=False):
        grabber_tab_depth = tab_depth - 0.5
        grabber_tab_inset = -0.5 * (-1 if flip_x else 1)
        grabber_tab_width = grabber_tab_depth * 2
        grabber_tab_radius = 1.4
        grabber_tab_margin_y = 0.3
        grabber_tab_margin_z = 0.4
        return minkowski()(
            translate(
                [
                    -grabber_tab_width * 0.5 + grabber_tab_radius + grabber_tab_inset,
                    hold_down_thickness
                    + tab_edge_offset
                    + grabber_tab_margin_y
                    + grabber_tab_radius,
                    tab_edge_offset
                    + grabber_tab_radius
                    + grabber_tab_margin_z
                    + cover_overhang_z,
                ]
            )(
                cube(
                    [
                        grabber_tab_width - grabber_tab_radius * 2,
                        tab_hole_size_y
                        - grabber_tab_margin_y * 2
                        - grabber_tab_radius * 2,
                        width
                        - tab_edge_offset * 2
                        - grabber_tab_radius * 2
                        - grabber_tab_margin_z * 2,
                    ]
                )
            ),
            sphere(r=grabber_tab_radius, segments=12),
        )

    grabber_arm_x = 1.5
    grabber_arm_y_offset = 1.5
    screw_hole_cover_grabber_tab_spacing = 2

    def grabber_arm(flip_x=False):
        grabber_arm_extend = 2
        grabber_arm_y = (
            wire_holder_thickness
            - (hold_down_thickness + grabber_tab_spacing)
            + grabber_arm_extend
            - grabber_arm_y_offset
        )

        return translate(
            [0, hold_down_thickness + grabber_tab_spacing + grabber_arm_y_offset, 0]
        )(
            cube(
                [
                    grabber_arm_x,
                    grabber_arm_y,
                    cover_width,
                ]
            ),
            hole()(
                translate(
                    [
                        grabber_arm_x
                        if flip_x
                        else -screw_hole_cover_grabber_tab_spacing,
                        0,
                        -1,
                    ]
                )(
                    cube(
                        [
                            screw_hole_cover_grabber_tab_spacing,
                            grabber_arm_y,
                            cover_width + 2,
                        ]
                    )
                ),
                translate([-1 if flip_x else grabber_arm_x, 0, -1])(
                    cube(
                        [
                            1,
                            wire_holder_thickness
                            - (hold_down_thickness + grabber_tab_spacing)
                            - grabber_arm_y_offset,
                            cover_overhang_z + 1,
                        ]
                    )
                ),
                translate(
                    [-1 if flip_x else grabber_arm_x, 0, cover_width - cover_overhang_z]
                )(
                    cube(
                        [
                            1,
                            wire_holder_thickness
                            - (hold_down_thickness + grabber_tab_spacing)
                            - grabber_arm_y_offset,
                            cover_overhang_z + 1,
                        ]
                    )
                ),
            ),
        )

    def top():
        y_offset = 0.4

        screw_cover_cube_length = (
            hold_down_length
            - grabber_arm_x
            - grabber_tab_spacing
            - screw_hole_cover_grabber_tab_spacing
        )

        def screw_cover_cube():
            return (
                translate(
                    [
                        0,
                        hold_down_thickness
                        + grabber_arm_y_offset
                        + grabber_tab_spacing,
                        0,
                    ]
                )(
                    cube(
                        [
                            screw_cover_cube_length,
                            wire_holder_thickness
                            - hold_down_thickness
                            + 0.1
                            - grabber_arm_y_offset,
                            cover_width,
                        ]
                    )
                ),
            )

        top_length = hold_down_length * 2 + midsection_length
        top_length_w_overhang = top_length + cover_overhang_x * 2
        top_rad = 2

        def lip():
            lip_rad = cover_overhang_z * 1.5
            lip_y_offset = -3.8
            cyl_z_offset = -0.5
            cyl_rad_offset = -1
            return [
                translate(
                    [
                        0,
                        wire_holder_thickness
                        + y_offset
                        + cover_thickness
                        - lip_rad
                        + lip_y_offset,
                        0,
                    ]
                )(
                    translate([top_rad, top_rad, top_rad])(
                        minkowski()(
                            cube(
                                [
                                    top_length_w_overhang - top_rad * 2,
                                    lip_rad + top_rad + 1 - top_rad * 2,
                                    lip_rad - top_rad * 2,
                                ]
                            ),
                            sphere(r=top_rad, segments=segments),
                        )
                    )
                    - translate([-1, 0, lip_rad + cyl_z_offset])(
                        rotate(a=90, v=[0, 1, 0])(
                            cylinder(
                                r=lip_rad + cyl_rad_offset,
                                h=top_length_w_overhang + 2,
                                segments=segments,
                            )
                        )
                    )
                )
            ]

        top_holes = []

        # Texture
        top_holes += [
            translate(
                [
                    hold_down_length
                    + wire_spacing
                    + wire_rad
                    + i * (wire_spacing + wire_rad * 2),
                    wire_holder_thickness,
                    cover_width * 0.5,
                ]
            )(
                rotate(a=-90, v=[1, 0, 0])(
                    cylinder(
                        r=wire_rad * 0.8,
                        h=cover_thickness + y_offset,
                        segments=segments,
                    )
                )
            )
            for i in range(n_wires)
        ]

        return (
            union()(
                # Top
                translate([-cover_overhang_x, wire_holder_thickness + y_offset, 0])(
                    translate([top_rad, top_rad, top_rad])(
                        minkowski()(
                            cube(
                                [
                                    top_length_w_overhang - top_rad * 2,
                                    cover_thickness - top_rad * 2,
                                    cover_width - top_rad * 2,
                                ]
                            ),
                            sphere(r=top_rad, segments=segments),
                        )
                    )
                ),
                # first screw cover
                translate([0, 0, 0])(screw_cover_cube()),
                translate([top_length - screw_cover_cube_length, 0, 0])(
                    screw_cover_cube()
                ),
                # bottom lip
                translate([-cover_overhang_x, 0, 0])(lip()),
                translate([-cover_overhang_x, 0, cover_width])(
                    scale([1, 1, -1])(lip())
                ),
            )
            - top_holes
        )

    return union()(
        translate([hold_down_length - grabber_tab_spacing, 0, 0])(
            grabber_piece() + left(grabber_arm_x)(grabber_arm())
        ),
        translate([hold_down_length + midsection_length + grabber_tab_spacing, 0, 0])(
            grabber_piece(flip_x=True) + grabber_arm(flip_x=True)
        ),
        top(),
    )


parts.append(bottom_part())

# parts.append(down(cover_overhang_z)(cap()))
parts.append(back(cover_thickness + wire_holder_thickness + 2)(cap()))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
