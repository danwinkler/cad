import math

from shapely.geometry import Polygon as ShapelyPolygon
from solid import *
from solid.utils import *

from cad.common.helper import *

in_to_mm = 25.4

insert_measured_diameter = 10.77
insert_measured_thread_diameter = 12.6


def build_cover():
    # 12 was a pretty okay fit for the smooth part
    # 12.5 was too small for the threads
    # diameters_to_test = [11, 12, 12.5]
    diameters_to_test = [12.75, 13, 13.25]

    # 12.75 is the winner!

    d_between = 18
    part = cube([len(diameters_to_test) * d_between, 20, 15])

    for i, diameter in enumerate(diameters_to_test):
        part -= translate([(i + 0.5) * d_between, 10, -1])(
            cylinder(d=diameter, h=22, segments=90)
        )

    # Cut a hole to make it easier to remove from the bed lol
    part -= translate([d_between - 2, -1, -1])(cube([4, 7, 5]))

    return part


parts = []

parts.append(build_cover())

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
