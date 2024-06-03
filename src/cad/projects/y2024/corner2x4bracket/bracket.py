import math
import pathlib
import random
import subprocess
from dataclasses import dataclass

import cv2
import euclid3
import numpy as np
import shapelysmooth
import solid
import svgpath2mpl
import ziafont
from bezier.curve import Curve
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

import cad.common
from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)


def arc(start_angle, end_angle, radius, center=(0, 0)):
    num_points = 100
    points = []
    for i in range(num_points + 1):
        angle = start_angle + (end_angle - start_angle) * i / num_points
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        points.append((x, y))
    return LineString(points)


in_to_mm = 25.4


class Bracket:
    def __init__(self):
        pass

    def generate_curve_as_linestring(self, nodes, num_points=100):
        nodes = np.asfortranarray(nodes).T  # Transpose to fit the expected input format

        curve = Curve.from_nodes(nodes)
        points = curve.evaluate_multi(np.linspace(0, 1, num_points)).T

        points = [tuple(p[:2]) for p in points]
        return LineString(points)

    def get_multi_model(self):
        model = MultipartModel(5)

        model.default_thickness = 1 / 4 * in_to_mm
        model.perimeter_bounds = (0, 0, 5800, 2750)

        m = Model()

        xd = 5 * in_to_mm
        yd = 6.5 * in_to_mm
        y_width = 1.5 * in_to_mm
        x_width = 3 * in_to_mm
        x_screw_rows = 2

        # Make a rectangle
        part = box(0, 0, xd, yd)

        # Subtract an ellipse with x radius xd and y radius yd
        ellipse = Point(xd, yd).buffer(xd)
        # Scale the circle so that it is an ellipse
        ellipse = scale(ellipse, xfact=1, yfact=yd / xd, origin=(xd, yd))

        part = part.difference(ellipse)

        # Expand the part
        part = part.buffer(min(x_width, y_width))

        part = Point(0, 0)

        curve = self.generate_curve_as_linestring(
            [(y_width, yd), (y_width, x_width), (xd, x_width)]
        )

        curve_part = Polygon([(xd, 0), (0, 0), (0, yd)] + list(curve.coords))

        part = unary_union(
            [
                curve_part,
                LineString([(0, 0), (xd, 0)]).buffer(x_width),
                LineString([(0, 0), (0, yd)]).buffer(y_width),
            ]
        )

        # Subtract from negative quadrants
        part -= box(-300, -300, 0, 300)
        part -= box(-300, -300, 300, 0)

        # Subtract screw holes
        screw_radius = 1 / 16 * in_to_mm

        n_screws = 3
        for i in range(n_screws):
            # Y axis screws
            part -= Point(y_width / 2, yd / (n_screws) * (i + 1)).buffer(screw_radius)

            # X axis screws
            for j in range(x_screw_rows):
                part -= Point(
                    (xd + x_width * 0.5) / (n_screws) * (i + 1),
                    x_width / (x_screw_rows * (j + 1)),
                ).buffer(screw_radius)

        m.add_poly(part)

        model.add_model(m)

        return model


m = Bracket()

model = m.get_multi_model()

top_level_geom = model.render_scad()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
# model.render_parts(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
