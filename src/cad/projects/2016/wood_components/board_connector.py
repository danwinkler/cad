import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

board_2x4_width = 89
board_2x4_height = 38

wall_thickness = 5
buffer_room = 1

connector_2_angle = 45

connector_height = board_2x4_height + wall_thickness * 2 + buffer_room * 2
connector_depth = board_2x4_width + wall_thickness * 2 + buffer_room * 2
connector_length = 100

connector_2_sin = math.sin(math.radians(connector_2_angle))
connector_2_cos = math.cos(math.radians(connector_2_angle))
connector_2_x_offset = connector_2_cos * connector_height
connector_2_y_offset = connector_2_sin * connector_height

parts = []

connector = cube([connector_length, connector_depth, connector_height])
connector_cutout = translate([-1, wall_thickness, wall_thickness])(
    cube(
        [
            connector_length + 2,
            board_2x4_width + buffer_room * 2,
            board_2x4_height + buffer_room * 2,
        ]
    )
)

connector_a = connector.copy()
connector_a_cutout = connector_cutout.copy()

connector_b = translate([connector_2_x_offset, 0, connector_height])(
    rotate(v=[0, 1, 0], a=-connector_2_angle)(connector.copy())
)

connector_b_cutout = translate([connector_2_x_offset, 0, connector_height])(
    rotate(v=[0, 1, 0], a=-connector_2_angle)(connector_cutout.copy())
)


full_connector = connector_a + connector_b
full_connector += cube(
    [connector_length, connector_depth, connector_height + connector_2_y_offset]
)
full_connector += translate([connector_length / 2.0, 0, 0])(
    cube(
        [
            connector_length / 2.0,
            connector_depth,
            connector_height + connector_2_sin * connector_length,
        ]
    )
)

full_connector -= connector_a_cutout
full_connector -= connector_b_cutout

screw_hole_short_x = connector_length / 3.0
screw_hole_long_x = screw_hole_short_x * 2
screw_hole_y = connector_depth / 3.0
screw_head = down(1.5)(cylinder(segments=12, r1=8, r2=0, h=3))
screw_hole_short = cylinder(
    segments=12,
    r=2,
    h=connector_height
    + connector_2_sin * (screw_hole_short_x - connector_2_x_offset)
    + connector_2_sin * connector_depth * 0.5,
)
screw_hole_long = cylinder(
    segments=12,
    r=2,
    h=connector_height
    + connector_2_sin * (screw_hole_long_x - connector_2_x_offset)
    + connector_2_sin * connector_depth * 0.5,
)
screw_hole_short += screw_head.copy()
screw_hole_long += screw_head.copy()

full_connector -= translate([screw_hole_short_x, screw_hole_y, 0])(
    screw_hole_short.copy()
)
full_connector -= translate([screw_hole_short_x, screw_hole_y * 2, 0])(
    screw_hole_short.copy()
)
full_connector -= translate([screw_hole_long_x, screw_hole_y, 0])(
    screw_hole_long.copy()
)
full_connector -= translate([screw_hole_long_x, screw_hole_y * 2, 0])(
    screw_hole_long.copy()
)

parts.append(full_connector)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
