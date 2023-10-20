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

# from cad.common.helper import *


# random.seed(0)


class Structure:
    def __init__(self):
        # Global settings
        self.wood_thickness = 5

    def wood_thickness_tab_hole_size(self):
        # This is so if we need to adjust the size of the hole separately from the wood_thickness variable
        # Ex. for kerf adjustment
        return self.wood_thickness - 0.2

    def get_multi_model(self):
        model = MultipartModel(thickness=self.wood_thickness)

        return model


structure = Structure()

model = structure.get_multi_model()

top_level_geom = model.render_full()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")

# model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")
model.render_dxfs(output_dir)

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
