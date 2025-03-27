import math

from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *


def build_cover():
    def build_dome_shape(dome_rad, wall_height=5):
        segments = 100
        dome = sphere(dome_rad, segments=segments) + rotate(v=[1, 0, 0], a=90)(
            cylinder(r=dome_rad, h=dome_rad, segments=segments)
        )

        # Cut bottom off
        # By cutting off a bit lower (wall_height - 1), we avoid rendering issues in openscad in the preview renderer
        dome -= translate([0, 0, -dome_rad - wall_height + 1])(
            cylinder(r=100, h=dome_rad)
        )

        # Cut a bit of the top off
        # dome -= translate([0, 0, dome_rad - 2])(cylinder(r=100, h=dome_rad))

        # Bring the sides down a bit
        dome += translate([0, 0, -wall_height])(
            cylinder(r=dome_rad, h=wall_height, segments=segments)
        )
        dome += translate([-dome_rad, -dome_rad, -wall_height])(
            cube([dome_rad * 2, dome_rad, wall_height])
        )

        return dome

    wall_height = 5

    outer_rad = 40
    inner_rad = outer_rad - 2

    outer_dome = build_dome_shape(outer_rad, wall_height=wall_height)

    inner_dome = build_dome_shape(inner_rad, wall_height=wall_height + 1)

    shape = outer_dome - inner_dome

    ledge_height = 4
    ledge_lip_height = 1.5
    ledge_lip_width = 2

    ledge_size = 50

    def make_ledge_connector():
        connector_width = outer_rad - ledge_size / 2
        connector_length = 25
        y_offset = connector_length - (ledge_size - outer_rad)
        connector = translate([0, -y_offset, 0])(
            cube([connector_width, connector_length, ledge_height + ledge_lip_height])
        )

        connector -= translate([connector_width, -y_offset, -1])(
            scale([connector_width, connector_length - 2, 1])(
                cylinder(r=1, h=ledge_height + ledge_lip_height + 2, segments=100)
            )
        )

        return connector

    ledge = translate([0, 0, -wall_height])(
        translate([-ledge_size / 2, -outer_rad, 0])(
            cube([ledge_size, ledge_size, ledge_height + ledge_lip_height])
        )
        + intersection()(
            translate([ledge_size / 2, 0, 0])(make_ledge_connector()), outer_dome
        )
        + intersection()(
            translate([-ledge_size / 2, 0, 0])(
                scale([-1, 1, 1])(make_ledge_connector())
            ),
            outer_dome,
        )
    )

    # This transformation creates a smaller ledge that we can subtract from the main ledge to
    # create a lip such that the themometer doesn't fall out
    ledge -= translate([0, 0, -wall_height + ledge_height])(
        linear_extrude(ledge_height + 1)(offset(-ledge_lip_width)(projection()(ledge)))
    )

    shape += ledge

    return shape


parts = []

parts.append(build_cover())

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
