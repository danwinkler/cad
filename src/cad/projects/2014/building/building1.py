import math
import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *

window_spacing_x = 20
window_spacing_y = 20
window_size_x = 8
window_size_y = 8
window_sil_size = 2

lip_depth = 1
lip_height = 3

width = 100
height = 200
length = 100

pillar_base_width = 10
pillar_base_top_width = 6
pillar_base_height = 2
pillar_count = 6

door_width = 10
door_height = 14
door_depth = 5


def pillar(height):
    pillar_top_offset = (pillar_base_width - pillar_base_top_width) / 2.0
    return union()(
        hull()(
            cube([pillar_base_width, pillar_base_width, 0.01]),
            translate([pillar_top_offset, pillar_top_offset, pillar_base_height])(
                cube([pillar_base_top_width, pillar_base_top_width, 0.01])
            ),
        ),
        translate([pillar_top_offset, pillar_top_offset, 0])(
            cube([pillar_base_top_width, pillar_base_top_width, height])
        ),
        up(height)(
            hull()(
                cube([pillar_base_width, pillar_base_width, 0.01]),
                translate([pillar_top_offset, pillar_top_offset, -pillar_base_height])(
                    cube([pillar_base_top_width, pillar_base_top_width, 0.01]),
                ),
            )
        ),
    )


def facade(face_width, face_height):
    windows = []
    holes = []
    x_rows = int(face_width / window_spacing_x)
    y_rows = int(face_height / window_spacing_y)
    dx = float(face_width) / x_rows
    dy = float(face_height) / y_rows
    for x in range(x_rows):
        for y in range(2, y_rows):
            windows.append(
                translate([x * dx + dx / 2.0, 0, y * dy + dy / 2.0])(
                    cube(size=[window_size_x, 1, window_size_y], center=True)
                )
            )
            holes.append(
                translate([x * dx + dx / 2.0, 0, y * dy + dy / 2.0])(
                    cube(
                        size=[
                            window_size_x - window_sil_size,
                            10,
                            window_size_y - window_sil_size,
                        ],
                        center=True,
                    )
                )
            )

    pillars = []
    pdx = (face_width - pillar_base_width) / (pillar_count - 1)

    for x in range(pillar_count - 1):
        pos = float(x) / pillar_count
        if pos < 0.3 or pos > 0.6:
            pillars.append(right(pdx * x)(pillar(dy * 2)))

    pillars.append(
        difference()(
            union()(
                translate([pillar_base_width * 1.5, pillar_base_width * 1.5, 0])(
                    cube([face_width - pillar_base_width * 3, 20, dy * 2 + 4])
                ),
                translate(
                    [
                        face_width / 2.0 - door_width / 2.0 - 2,
                        pillar_base_width * 1.5 - 2,
                        0,
                    ]
                )(cube([door_width + 4, door_depth + 1, door_height + 2])),
            ),
            translate(
                [
                    face_width / 2.0 - door_width / 2.0,
                    pillar_base_width * 1.5 - 5,
                    0.001,
                ]
            )(cube([door_width, door_depth + 5, door_height])),
        )
    )

    pillars.append(up(dx * 2 + 4)(cube([face_width, pillar_base_width * 1.5 + 20, 2])))

    return union()(
        union()(windows),
        up(dy * 2)(cube([face_width, 3, face_height - dy * 2])),
        lip(face_width, dy * 2 + lip_height / 2.0),
        lip(face_width, face_height - dy * 2),
        lip(face_width, face_height),
        lip(face_width, face_height + 3),
        union()(pillars),
    ) - union()(holes)


def lip(width, height):
    return translate([-lip_depth, -lip_depth, height - lip_height / 2.0])(
        cube([width + lip_depth * 2, lip_depth + 1, lip_height])
    )


parts = []

parts.append(union()(facade(width, height)))
parts.append(translate([width, 0, 0])(rotate(90, [0, 0, 1])(facade(length, height))))
parts.append(
    translate([width, length, 0])(rotate(180, [0, 0, 1])(facade(width, height)))
)
parts.append(translate([0, length, 0])(rotate(270, [0, 0, 1])(facade(length, height))))

# parts.append( translate( [width/2 - 10, length/2- 10, 0] ) ( cube( [20,20,height] ) ) )
# parts.append( translate( [0, 0, height-3] ) ( cube( [width,length,3] ) ) )

for i in range(1, 4):
    parts.append(
        translate([-i * 2, -i * 2, -i * 2])(
            cube([width + i * 2 * 2, length + i * 2 * 2, 2])
        )
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
