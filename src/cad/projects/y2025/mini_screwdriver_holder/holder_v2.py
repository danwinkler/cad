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
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils
from solid.objects import cylinder, polyhedron
from solid.objects import translate as s_translate
from solid.objects import union

from cad.common.helper import Vec3, vine
from cad.common.lasercut import Model, MultipartModel, SolidModel, s_poly_to_scad
from cad.projects.y2025.mini_screwdriver_holder.loft import loft_polygons

tip_length = 14
tip_rad = 1
handle_rad = 2.25


def zero_slope_cubic(x, x1, y1, x2, y2):
    """
    Hermite cubic with zero endpoint slopes.
    x can be a scalar or numpy array.
    """
    t = (x - x1) / (x2 - x1)
    # Hermite basis with zero tangents
    h00 = 2 * t**3 - 3 * t**2 + 1
    h01 = -2 * t**3 + 3 * t**2
    return y1 * h00 + y2 * h01


def get_model():
    model = MultipartModel()

    bottom_rad = 32

    screw_rad = 2.9
    top_rad = screw_rad + 5
    top_z = 30

    layer_height = 2

    shape_model = SolidModel()

    parts = []

    def width_function(z_i, a):
        if z_i < top_z - 8:
            return zero_slope_cubic(z_i, 0, bottom_rad, top_z - 8, top_rad)
        else:
            return top_rad

    base = vine(
        [Vec3(0, 0, z) for z in range(0, top_z + 1)], width_function, sections=64
    )

    screw_hole = s_translate([0, 0, top_z - 20])(
        cylinder(r=screw_rad + 0.1, h=40, segments=36)
    )

    cutout_rad = bottom_rad - 10

    show_tips = False
    if show_tips:
        for i in range(12):
            a = i * (math.pi * 2 / 12)
            cutout = s_translate(
                [
                    math.cos(a) * (cutout_rad),
                    math.sin(a) * (cutout_rad),
                    top_z + 4.9 - tip_length,
                ]
            )(cylinder(r=tip_rad + 0.1, h=tip_length, segments=12))
            base = base + cutout

    base = base - screw_hole

    # Cut out a cone underneath so it doesn't stick to the bed so hard/makes printing faster

    undercut = s_translate([0, 0, -1])(
        cylinder(r1=bottom_rad - 8, r2=screw_rad + 0.1, h=15.1, segments=36)
    )
    base = base - undercut

    shape_model.add_solid(base)

    model.add_model(shape_model)

    bottom_ring_model = Model()
    bottom_ring_shape = Point(0, 0).buffer(bottom_rad + 2)
    bottom_ring_shape -= Point(0, 0).buffer(screw_rad + 0.5)

    for i in range(12):
        a = i * (math.pi * 2 / 12)
        cutout = Point(math.cos(a) * cutout_rad, math.sin(a) * cutout_rad).buffer(
            tip_rad + 0.5
        )
        bottom_ring_shape = bottom_ring_shape - cutout

    bottom_ring_model.add_poly(bottom_ring_shape)
    bottom_ring_model.thickness = 4.9
    bottom_ring_model.renderer.translate(z=top_z).color(0.8, 0.7, 0.2)
    model.add_model(bottom_ring_model)

    top_ring_model = Model()
    top_ring_shape = Point(0, 0).buffer(bottom_rad + 2)
    top_ring_shape -= Point(0, 0).buffer(handle_rad + 0.5)

    for i in range(12):
        a = i * (math.pi * 2 / 12)
        cutout = Point(math.cos(a) * cutout_rad, math.sin(a) * cutout_rad).buffer(
            handle_rad + 0.5
        )
        top_ring_shape = top_ring_shape - cutout

    top_ring_model.add_poly(top_ring_shape)
    top_ring_model.thickness = 4.9
    top_ring_model.renderer.translate(
        z=(top_z - 10) + 60 - top_ring_model.thickness
    ).color(0.7, 0.4, 0.1)
    model.add_model(top_ring_model)

    show_screw = True
    if show_screw:
        screw = s_translate([0, 0, top_z - 10])(
            cylinder(r=screw_rad, h=60, segments=36)
        )
        screw_model = SolidModel()
        screw_model.add_solid(screw)
        model.add_model(screw_model).renderer.color(0.5, 0.5, 0.5)

    return model


if __name__ == "__main__":
    model = get_model()

    output_dir = pathlib.Path(__file__).parent / (
        pathlib.Path(__file__).stem + "_parts"
    )
    model.render_parts(output_dir)
    model.render_single_dxf(output_dir / "single.dxf")
    top_level_geom = model.render_scad()
    print(f"Total Cut Length: {model.get_total_cut_length()}")
    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(solid.scad_render(top_level_geom))
