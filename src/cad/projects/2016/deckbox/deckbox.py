from solid import *
from solid.utils import *

from cad.common.helper import *

width = 73
height = 100
length = 47
wall_thickness = 5
thin_wall = 2
inverse_wall = wall_thickness - thin_wall

front_height = 50
back_height = 70

parts = []

angled_cut = translate([-1, 0, front_height + wall_thickness])(
    rotate(v=[0, 0, 1], a=90)(
        rotate(v=[1, 0, 0], a=90)(
            linear_extrude(height=width + wall_thickness * 2 + 2)(
                polygon(
                    points=[
                        [-1, 0],
                        [wall_thickness, 0],
                        [length + wall_thickness, back_height - front_height],
                        [length + wall_thickness, 100],
                        [-1, 100],
                    ],
                    paths=[[0, 1, 2, 3, 4]],
                )
            )
        )
    )
)

base = cube(
    [
        width + wall_thickness * 2,
        length + wall_thickness * 2,
        back_height + wall_thickness,
    ]
)
base -= angled_cut
base -= translate([-1, -1, front_height + wall_thickness])(
    cube([1 + inverse_wall, 2 + length * wall_thickness * 2, 100])
)
base -= translate(
    [width + wall_thickness + thin_wall, -1, front_height + wall_thickness]
)(cube([1 + inverse_wall, 2 + length * wall_thickness * 2, 100]))
base -= translate(
    [-1, wall_thickness + length + thin_wall, front_height + wall_thickness]
)(cube([2 + wall_thickness * 2 + width, inverse_wall + 1, 100]))
base += translate(
    [
        wall_thickness + width / 2,
        length + wall_thickness + 0.5,
        wall_thickness + (front_height + back_height) / 2.0,
    ]
)(sphere(segments=20, r=3))
base -= translate([wall_thickness, wall_thickness, wall_thickness])(
    cube([width, length, height])
)

top_angled_cut = translate([thin_wall, 0, front_height + wall_thickness])(
    rotate(v=[0, 0, 1], a=90)(
        rotate(v=[1, 0, 0], a=90)(
            linear_extrude(height=width + inverse_wall * 2)(
                polygon(
                    points=[
                        [wall_thickness, -2],
                        [wall_thickness + inverse_wall + length, -2],
                        [
                            wall_thickness + inverse_wall + length,
                            back_height - front_height,
                        ],
                        [wall_thickness, 0],
                    ],
                    paths=[[0, 1, 2, 3]],
                )
            )
        )
    )
)


top = translate([0, 0, front_height + wall_thickness])(
    cube(
        [
            width + wall_thickness * 2,
            length + wall_thickness * 2,
            height - front_height + wall_thickness,
        ]
    )
)
top -= translate([wall_thickness, wall_thickness, wall_thickness])(
    cube([width, length, height])
)
top -= top_angled_cut
top -= translate(
    [
        wall_thickness + width / 2,
        length + wall_thickness + 0.5 + 0.5,
        wall_thickness + (front_height + back_height) / 2.0,
    ]
)(sphere(segments=20, r=3))

parts.append(base)

parts.append(translate([-(width + wall_thickness * 2 + 5), 0, 1])(top))

print("Saving File")
with open(__file__ + "base" + ".scad", "w") as f:
    f.write(scad_render(union()(base)))

with open(__file__ + "top" + ".scad", "w") as f:
    f.write(scad_render(union()(top)))
