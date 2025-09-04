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


# TODO: This isn't watertight for some reason. maybe loft.py is broken
def circle_to_circle_loft(rad0, rad1, z0, z1, layer_height):
    layers = []

    for i in range(z0, z1, layer_height):
        d0 = zero_slope_cubic(i, z0, rad0, z1, rad1)
        d1 = zero_slope_cubic(i + layer_height, z0, rad0, z1, rad1)

        base = Point(0, 0).buffer(d0)

        top = Point(0, 0).buffer(d1)

        vertices, faces = loft_polygons(base, top, z0=i, z1=i + layer_height + 0.01)

        shape = polyhedron(points=vertices, faces=faces)

        layers.append(shape)

    return union()(layers)


# Ugh this fucking design looks terrible
def get_model():
    model = MultipartModel()

    bottom_rad = 40
    waist_rad = 12.5
    waist_z = 25

    wide_top_rad = 35
    wide_top_z = 45

    top_rad = 5
    top_z = 80

    layer_height = 2

    shape_model = SolidModel()

    parts = []

    # parts.append(circle_to_circle_loft(bottom_rad, waist_rad, 0, waist_z, layer_height))

    # parts.append(
    #     circle_to_circle_loft(
    #         waist_rad, wide_top_rad, waist_z, wide_top_z, layer_height
    #     )
    # )

    # parts.append(
    #     circle_to_circle_loft(wide_top_rad, top_rad, wide_top_z, top_z, layer_height)
    # )

    def width_function(z_i, a):
        if z_i < waist_z:
            return zero_slope_cubic(z_i, 0, bottom_rad, waist_z, waist_rad)
        elif z_i < wide_top_z:
            return zero_slope_cubic(z_i, waist_z, waist_rad, wide_top_z, wide_top_rad)
        else:
            return zero_slope_cubic(z_i, wide_top_z, wide_top_rad, top_z, top_rad)

    # main = union()(parts)

    main = vine(
        [Vec3(0, 0, z) for z in range(0, top_z + 1)], width_function, sections=64
    )

    cutouts = []

    cutout_rad = wide_top_rad - 10

    for i in range(12):
        a = i * (math.pi * 2 / 12)
        tip_cutout = s_translate(
            [
                math.cos(a) * cutout_rad,
                math.sin(a) * cutout_rad,
                wide_top_z - tip_length,
            ]
        )(cylinder(r=tip_rad + 0.5, h=tip_length, segments=36))

        handle_cutout = s_translate(
            [math.cos(a) * cutout_rad, math.sin(a) * cutout_rad, wide_top_z]
        )(cylinder(r=handle_rad + 0.5, h=40, segments=36))

        cutouts.append(tip_cutout + handle_cutout)

    main = main - union()(cutouts)

    shape_model.add_solid(main)

    model.add_model(shape_model)

    return model


if __name__ == "__main__":
    model = get_model()

    output_dir = pathlib.Path(__file__).parent / (
        pathlib.Path(__file__).stem + "_parts"
    )
    # model.render_parts(output_dir)
    # model.render_single_dxf(output_dir / "single.dxf")
    top_level_geom = model.render_scad()
    print(f"Total Cut Length: {model.get_total_cut_length()}")
    print("Saving File")
    with open(__file__ + ".scad", "w") as f:
        f.write(solid.scad_render(top_level_geom))
