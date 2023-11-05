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
from cad.common.lasercut import Model, MultipartModel, s_poly_to_scad, skeleton_to_polys
from cad.common.project_step import ProjectSteps

project_steps = ProjectSteps()

outline = Point(0, 0).buffer(200) - Point(0, 0).buffer(100)
rim = outline - outline.buffer(-5)

project_steps.record(outline, key="outline")

for i in range(2, 200, 2):
    infill = honeycomb_a.get_honeycomb_structure_for_poly(
        outline,
        honeycomb_regions=i,
        honeycomb_scale=10,
        region_min=2,
        region_max=6,
        wall_offset=-1.5,
    )

    shape = unary_union([rim, outline - infill])

    min_area = 8
    shape = Polygon(
        shape.exterior.coords,
        [i for i in shape.interiors if Polygon(i).area > min_area],
    )

    project_steps.record(shape, key=f"shape_{i:03d}")

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_steps")
output_dir.mkdir(exist_ok=True)

project_steps.render(output_dir)
