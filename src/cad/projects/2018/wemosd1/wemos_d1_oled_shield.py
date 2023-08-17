import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

SEGMENTS = 12


class Wemos:
    width = 25.6
    length = 34.4
    depth = 0.9

    header_y_offset = 7
    header_thickness = 2.45
    header_height = 9.5
    header_length = 20.9

    hole_radius = 1.05

    hole_offset = 3.2
    hole_back_offset = 3.5

    def render(self):
        base = cube([self.width, self.length, self.depth])

        header = cube([self.header_thickness, self.header_length, self.header_height])
        header_left = translate([0, self.header_y_offset, self.depth])(header)
        header_right = translate(
            [self.width - self.header_thickness, self.header_y_offset, self.depth]
        )(header)

        screw_hole = down(0.5)(
            cylinder(r=self.hole_radius, h=self.depth + 1, segments=SEGMENTS)
        )

        screw_hole_a = translate(
            [self.hole_offset, self.length - self.hole_back_offset, 0]
        )(screw_hole)
        screw_hole_b = translate([self.width - self.hole_offset, self.hole_offset, 0])(
            screw_hole
        )

        return union()(base, header_left, header_right) - (screw_hole_a + screw_hole_b)


class WemosOLEDShield:
    width = Wemos.width
    length = 29.6
    depth = Wemos.depth

    bottom_header_offset = 2.6
    screen_height = 3.1

    screen_y_offset = 14
    screen_x_offset = 5
    screen_y_size = 13
    screen_x_size = width - (screen_x_offset * 2)

    def render(self):
        base = cube([self.width, self.length, self.depth])

        return base


height_to_screen = (
    Wemos.depth
    + Wemos.header_height
    + WemosOLEDShield.bottom_header_offset
    + WemosOLEDShield.depth
    + WemosOLEDShield.screen_height
)


class Case:
    floor_thickness = 3
    wall_thickness = 3
    top_thickness = 3
    board_margin = 1
    board_z_offset = 7

    wall_height = board_z_offset + height_to_screen + 3

    width = Wemos.width + board_margin * 2 + wall_thickness * 2
    length = Wemos.length + board_margin * 2 + wall_thickness * 2

    usb_hole_height = 12
    usb_hole_width = 14

    usb_hole_z_offset = 4

    button_y_offset = wall_thickness + board_margin + 3.5
    button_z_offset = (
        board_z_offset
        + Wemos.depth
        + Wemos.header_height
        + WemosOLEDShield.bottom_header_offset
        - 2
    )
    button_stem_width = 3
    button_stem_thickness = 2.5
    button_top_rad = 2

    button_gap = 0.8
    button_gap_shape = rotate(a=90, v=[0, 1, 0])(
        cylinder(h=wall_thickness + 1, r=button_gap, segments=SEGMENTS)
    )

    button_gap_z_start = floor_thickness + board_z_offset
    button_gap_prevent = translate([-5, -5, 0])(cube([20, 20, button_gap_z_start]))

    screw_hole_rad = 0.7
    screw_hole_base_size = board_margin + 6

    def render(self):
        def wall(w, l, h, r):
            r = r * 0.9999999
            return minkowski()(
                translate([r, r, r])(cube([w - r * 2, l - r * 2, h - r * 2])),
                sphere(r=r, segments=SEGMENTS),
            )

        base = wall(
            self.width, self.length, self.floor_thickness, self.floor_thickness * 0.5
        )

        usb_hole = translate(
            [
                self.width * 0.5 - (self.usb_hole_width * 0.5),
                -0.5,
                self.floor_thickness + self.usb_hole_z_offset,
            ]
        )(cube([self.usb_hole_width, self.wall_thickness + 1, self.usb_hole_height]))

        front_wall = (
            wall(
                self.width,
                self.wall_thickness,
                self.floor_thickness + self.wall_height,
                self.wall_thickness * 0.5,
            )
            - usb_hole
        )
        back_wall = forward(self.length - self.wall_thickness)(
            wall(
                self.width,
                self.wall_thickness,
                self.floor_thickness + self.wall_height,
                self.wall_thickness * 0.5,
            )
        )

        side_wall = wall(
            self.wall_thickness,
            self.length,
            self.floor_thickness + self.wall_height,
            self.wall_thickness * 0.5,
        )

        button_shape = right((self.wall_thickness - self.button_stem_thickness) * 0.5)(
            cube(
                [
                    self.button_stem_thickness,
                    self.button_stem_width,
                    self.button_z_offset,
                ]
            )
        )
        button_shape += translate(
            [0, self.button_stem_width * 0.5, self.button_z_offset]
        )(
            scale([0.75, 1.03, 1.03])(
                rotate(a=90, v=[0, 1, 0])(
                    sphere(r=self.button_top_rad, segments=SEGMENTS)
                )
            ),
            right(self.wall_thickness)(
                scale([1, 1.03, 1.03])(
                    rotate(a=90, v=[0, 1, 0])(
                        sphere(r=self.button_top_rad, segments=SEGMENTS)
                    )
                )
            ),
            rotate(a=90, v=[0, 1, 0])(
                cylinder(
                    r=self.button_top_rad, h=self.wall_thickness, segments=SEGMENTS
                )
            ),
        )

        button_shape = up(self.floor_thickness)(button_shape)

        side_wall -= translate(
            [-1, self.button_y_offset - self.button_stem_width * 0.5, 0]
        )(minkowski()(button_shape, self.button_gap_shape) - self.button_gap_prevent)

        side_wall += translate(
            [0, self.button_y_offset - self.button_stem_width * 0.5, 0]
        )(button_shape)

        def screw_hole_base(hole=True):
            screw_hole_base = cube(
                [
                    self.screw_hole_base_size,
                    self.screw_hole_base_size,
                    self.board_z_offset + Wemos.depth,
                ]
            )
            if hole:
                screw_hole_base -= translate(
                    [
                        self.board_margin + Wemos.hole_offset,
                        self.board_margin + Wemos.hole_offset,
                        -1,
                    ]
                )(
                    cylinder(
                        r=self.screw_hole_rad,
                        h=self.board_z_offset + Wemos.depth + 2,
                        segments=SEGMENTS,
                    )
                )
            screw_hole_base -= translate(
                [
                    self.board_margin - 0.2,
                    self.board_margin - 0.2,
                    self.board_z_offset - 0.1,
                ]
            )(
                cube(
                    [
                        self.screw_hole_base_size,
                        self.screw_hole_base_size,
                        Wemos.depth + 1,
                    ]
                )
            )
            return screw_hole_base

        screw_hole_a = translate(
            [self.wall_thickness, self.wall_thickness, self.floor_thickness]
        )(screw_hole_base(False))
        screw_hole_b = translate(
            [
                self.width - self.wall_thickness,
                self.wall_thickness,
                self.floor_thickness,
            ]
        )(scale([-1, 1, 1])(screw_hole_base()))
        screw_hole_c = translate(
            [
                self.wall_thickness,
                self.length - self.wall_thickness,
                self.floor_thickness,
            ]
        )(scale([1, -1, 1])(screw_hole_base()))
        screw_hole_d = translate(
            [
                self.width - self.wall_thickness,
                self.length - self.wall_thickness,
                self.floor_thickness,
            ]
        )(scale([-1, -1, 1])(screw_hole_base(False)))

        top_inset = translate(
            [
                self.wall_thickness * 0.5,
                self.wall_thickness * 0.5,
                self.floor_thickness + self.wall_height - self.top_thickness,
            ]
        )(
            cube(
                [
                    self.width - self.wall_thickness,
                    self.length - self.wall_thickness,
                    self.top_thickness + 1,
                ]
            )
        )

        return (
            union()(
                base,
                front_wall,
                side_wall,
                translate([self.width, 0, 0])(scale([-1, 1, 1])(side_wall)),
                back_wall,
                screw_hole_a,
                screw_hole_b,
                screw_hole_c,
                screw_hole_d,
            )
            - top_inset
        )


class Top:
    def render(self):
        return translate([Case.wall_thickness * 0.5, Case.wall_thickness * 0.5, 0])(
            cube(
                [
                    Case.width - Case.wall_thickness,
                    Case.length - Case.wall_thickness,
                    Case.top_thickness,
                ]
            )
        ) - translate(
            [
                Case.wall_thickness
                + Case.board_margin
                + WemosOLEDShield.screen_x_offset,
                Case.wall_thickness
                + Case.board_margin
                + WemosOLEDShield.screen_y_offset,
            ]
        )(
            cube(
                [
                    WemosOLEDShield.screen_x_size,
                    WemosOLEDShield.screen_y_size,
                    Case.top_thickness,
                ]
            )
        )


parts.append(Case().render())

if False:
    parts.append(
        color([0, 0, 1])(
            translate(
                [
                    Case.wall_thickness + Case.board_margin,
                    Case.wall_thickness + Case.board_margin,
                    Case.floor_thickness + Case.board_z_offset,
                ]
            )(
                Wemos().render()
                + up(
                    Wemos.depth
                    + Wemos.header_height
                    + WemosOLEDShield.bottom_header_offset
                )(WemosOLEDShield().render())
            )
        )
    )

if False:
    parts.append(
        translate([0, 0, Case.floor_thickness + Case.wall_height - Case.top_thickness])(
            Top().render()
        )
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))

print("Saving File")
with open(__file__ + ".top.scad", "w") as f:
    f.write(scad_render(union()(Top().render())))
