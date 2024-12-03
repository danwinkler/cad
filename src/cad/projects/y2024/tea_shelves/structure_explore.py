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
from fontTools.ttLib import TTFont
from shapely import concave_hull
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.common.fills_2d import honeycomb_a
from cad.common.lasercut import (
    Model,
    MultipartModel,
    SolidModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)
from cad.common.project_step import ProjectSteps
from cad.projects.y2024.tea_shelves.joint_structure import structure


def in_to_mm(inches):
    return inches * 25.4


st = structure.Structure()
st.rect(0, 0, 0, 100, 100, 0)
st.rect(0, 0, 0, 40, 0, 60)


model = st.get_multi_model()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
# model.render_parts(output_dir)

top_level_geom = model.render_scad()

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
