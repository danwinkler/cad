from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

f_size = 20
m_size = 14

x_count = 8
y_count = 8

spar_height = 2
spar_width = 3
spar_length = 16

spar_height_diff = 2

spar_separation = 2

for x in range(x_count):
    for y in range(y_count):
        parts.append(
            translate(
                [
                    x * (spar_length + spar_separation)
                    + ((spar_length / 2) + (spar_separation / 2) if y % 2 == 1 else 0),
                    y * (spar_length / 2 + spar_separation - spar_width / 2),
                    0,
                ]
            )(
                union()(
                    translate([-spar_length / 2, -spar_length / 2, 0])(
                        cube([spar_length, spar_width, spar_height])
                    ),
                    translate([-spar_length / 2, spar_length / 2 - spar_width, 0])(
                        cube([spar_length, spar_width, spar_height])
                    ),
                    translate(
                        [
                            -spar_length / 2,
                            -spar_length / 2,
                            spar_height + spar_height_diff,
                        ]
                    )(cube([spar_width, spar_length, spar_height])),
                    translate(
                        [
                            spar_length / 2 - spar_width,
                            -spar_length / 2,
                            spar_height + spar_height_diff,
                        ]
                    )(cube([spar_width, spar_length, spar_height])),
                    translate([-spar_length / 2, -spar_length / 2, spar_height])(
                        cube([spar_width, spar_width, spar_height_diff])
                    ),
                    translate(
                        [
                            spar_length / 2 - spar_width,
                            spar_length / 2 - spar_width,
                            spar_height,
                        ]
                    )(cube([spar_width, spar_width, spar_height_diff])),
                    translate(
                        [spar_length / 2 - spar_width, -spar_length / 2, spar_height]
                    )(cube([spar_width, spar_width, spar_height_diff])),
                    translate(
                        [-spar_length / 2, spar_length / 2 - spar_width, spar_height]
                    )(cube([spar_width, spar_width, spar_height_diff])),
                )
            )
        )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
