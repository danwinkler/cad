import boxscad

from solid import *

board_width = 40
board_length = 60

board_margin = 2

box_wall_thickness = 3

box_width = board_width + board_margin * 2 + box_wall_thickness * 2
box_length = board_length + board_margin * 2 + box_wall_thickness * 2
box_height = 55

hole_offset = 3
hole_radius = 1.2
standoff_length = 3.5

usb_hole_y_offset = standoff_length + 10
usb_hole_width = 15
usb_hole_height = 15

b = boxscad.RoundedBox(box_width, box_length, box_height, box_wall_thickness)

b.add_ornament(boxscad.Face.TOP, boxscad.ornaments.InsetLid(b.wall_thickness))

b.add_ornament(
    boxscad.Face.BOTTOM,
    boxscad.ornaments.StandOffs(
        board_width - (hole_offset * 2),
        board_length - (hole_offset * 2),
        standoff_length,
        hole_radius,
        wall_hole_depth=b.wall_thickness - 0.4,
    ),
)

b.add_ornament(
    boxscad.Face.BOTTOM,
    boxscad.ornaments.SquareHole(
        box_wall_thickness + board_margin + 15,
        box_wall_thickness + board_margin + 3,
        10,
        10,
    ),
)

b.add_ornament(
    boxscad.Face.FRONT,
    boxscad.ornaments.SquareHole(
        (box_width - usb_hole_width) * 0.5,
        usb_hole_y_offset,
        usb_hole_width,
        usb_hole_height,
    ),
)

scad_render_to_file(b.render(), "box2.scad")

boxscad.blueprint.blueprint("blueprint", b)
