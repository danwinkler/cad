import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

parts = []

aukey_width = 31
# The top slopes downwards, so it's taller in the back than the front
aukey_front_height = 34.5
aukey_back_height = 36

# Adjusted from 3d print
aukey_height = 34
aukey_depth = 36

aukey_margin = 0.25

wall_thickness = 2

inner_aukey_holder_width = aukey_width + aukey_margin * 2
inner_aukey_holder_height = (
    aukey_front_height + aukey_back_height
) / 2 + aukey_margin * 2
outer_aukey_holder_width = inner_aukey_holder_width + wall_thickness * 2
outer_aukey_holder_height = inner_aukey_holder_height + wall_thickness * 2
holder_depth = 26


def aukey_holder():
    return (
        cube(
            [
                outer_aukey_holder_width,
                outer_aukey_holder_height,
                holder_depth,
            ]
        )
        - translate([wall_thickness, wall_thickness, -1])(
            cube(
                [inner_aukey_holder_width, inner_aukey_holder_height, holder_depth + 2]
            )
        )
        - translate([outer_aukey_holder_width * 0.5, -EPSILON, holder_depth * 0.5])(
            rotate(a=-90, v=[1, 0, 0])(
                cylinder(
                    r=holder_depth * 0.5 - wall_thickness,
                    h=outer_aukey_holder_height + EPSILON * 2,
                )
            )
        )
    )


atom_height = 24
atom_depth = 9.6
atom_margin = 0.3
atom_plug_width = 15
atom_lip_size = 3
atom_plug_roundover = 3

atom_holder_total_y = wall_thickness + atom_height + atom_margin + wall_thickness


def atom_plug_hole(depth):
    return translate([atom_plug_roundover, 0, atom_plug_roundover])(
        minkowski()(
            cube(
                [
                    depth + atom_margin - (atom_plug_roundover * 2),
                    wall_thickness + EPSILON * 2,
                    atom_plug_width - (atom_plug_roundover * 2),
                ]
            ),
            rotate(a=90, v=[1, 0, 0])(
                cylinder(r=atom_plug_roundover, h=wall_thickness, segments=16)
            ),
        )
    )


def atom_holder():
    return union()(
        # Bottom
        cube([atom_depth + atom_margin + wall_thickness, wall_thickness, holder_depth]),
        translate([atom_depth + atom_margin, 0, 0])(
            cube([wall_thickness, wall_thickness + atom_lip_size, holder_depth])
        ),
        # Top
        translate([0, wall_thickness + atom_height + atom_margin])(
            cube(
                [
                    atom_depth + atom_margin + wall_thickness,
                    wall_thickness,
                    holder_depth,
                ]
            )
            - translate([0, -EPSILON, (holder_depth - atom_plug_width) * 0.5])(
                atom_plug_hole(atom_depth)
            ),
            translate([atom_depth + atom_margin, -atom_lip_size, 0])(
                cube([wall_thickness, wall_thickness + atom_lip_size, holder_depth])
            ),
        ),
    )


env_height = 32
env_depth = 8
env_margin = 0.3
env_holder_total_y = wall_thickness + env_height + env_margin + wall_thickness
env_holder_total_x = wall_thickness + env_depth + env_margin


def env_holder():
    return union()(
        # Bottom
        cube([env_depth + env_margin + wall_thickness, wall_thickness, holder_depth]),
        translate([0, 0, 0])(
            cube([wall_thickness, wall_thickness + atom_lip_size, holder_depth])
        ),
        # Top
        translate([0, wall_thickness + env_height + env_margin])(
            cube(
                [
                    env_depth + env_margin + wall_thickness,
                    wall_thickness,
                    holder_depth,
                ]
            )
            - translate(
                [wall_thickness, -EPSILON, (holder_depth - atom_plug_width) * 0.5]
            )(atom_plug_hole(env_depth)),
            translate([0, -atom_lip_size, 0])(
                cube([wall_thickness, wall_thickness + atom_lip_size, holder_depth])
            ),
        ),
    )


parts.append(aukey_holder())
parts.append(
    translate(
        [outer_aukey_holder_width, outer_aukey_holder_height - atom_holder_total_y, 0]
    )(atom_holder())
)
parts.append(
    translate([-env_holder_total_x, outer_aukey_holder_height - env_holder_total_y, 0])(
        env_holder()
    )
)
# parts.append(atom_plug_hole())

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
