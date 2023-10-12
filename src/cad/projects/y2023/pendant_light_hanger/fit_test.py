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
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.projects.y2023.pendant_light_hanger.common import (
    Model,
    MultipartModel,
    s_poly_to_scad,
    skeleton_to_polys,
)

# from cad.common.helper import *


random.seed(0)

model = MultipartModel()


def get_text_polygon(text):
    """
    For a given string returns a shapely polygon representing the text.

    Kind of ugly because I'm doing character layout myself
    """
    ttf_font = TTFont(str(pathlib.Path(__file__).parent / "Roboto-Regular.ttf"))

    # Create an empty list to store the glyph shapes
    glyph_shapes = []
    cur_x = 0

    # Iterate through each character in the text
    for char in text:
        glyph_name = ttf_font.getBestCmap()[ord(char)]
        glyph = ttf_font["glyf"][glyph_name]

        # Extract the glyph's contours
        if hasattr(glyph, "components"):
            # If the glyph has components, flatten them to a simple outline
            glyph = glyph.getCompositeGlyph()

        contour, indicies, flags = glyph.getCoordinates(ttf_font["glyf"])

        polygon = None
        cur_poly = []
        for i, coord in enumerate(contour):
            cur_poly.append((coord[0], coord[1]))

            if i in indicies:
                if polygon is None:
                    polygon = Polygon(cur_poly)
                else:
                    new_poly = LinearRing(cur_poly)

                    # TTF fonts define negative space as being CCW
                    if new_poly.is_ccw:
                        polygon -= Polygon(cur_poly)
                    else:
                        polygon = unary_union([polygon, Polygon(cur_poly)])

                cur_poly = []

        polygon = translate(polygon, cur_x, 0)
        cur_x = polygon.bounds[2]

        glyph_shapes.append(polygon)

    # Combine the individual glyph shapes into a MultiPolygon
    multipolygon = MultiPolygon(glyph_shapes)

    return multipolygon


def hole_size_test():
    hole_sizes = [4, 4.4, 4.5, 4.6, 5.0]

    margin = 5
    max_hole_size = max(hole_sizes)
    hole_interval = max_hole_size * 2 + margin
    height = max_hole_size * 2 + margin * 2
    width = hole_interval * (len(hole_sizes) + 1)

    base = box(0, 0, width, height)
    engrave_polys = []
    for i, hole_size in enumerate(hole_sizes):
        x_pos = hole_interval * (i + 1)
        base -= Point(x_pos, margin + max_hole_size).buffer(hole_size)

        text_scale = 0.002

        text_poly_scaled = scale(
            get_text_polygon(str(hole_size)),
            text_scale,
            text_scale,
            text_scale,
            origin=(0, 0),
        )

        # TODO: what I really want here is to add the text to a separate layer/group which will then be engraved instead of cut
        # To do this I need another primitive beside Polygon I think
        text = translate(
            text_poly_scaled,
            x_pos - text_poly_scaled.bounds[0] - text_poly_scaled.bounds[2] / 2,
            1,
        )

        engrave_polys.append(text)

    model = Model()
    model.add_poly(base)
    model.add_poly(unary_union(engrave_polys), color="red", thickness=6, layer="text")

    return model


def fit_test_a():
    slot_sizes = [2.9, 3.0, 3.1]

    margin = 5
    max_slot_size = max(slot_sizes)
    slot_interval = max_slot_size * 2 + margin
    slot_height = 6
    height = 20
    width = slot_interval * (len(slot_sizes) + 1)

    base = box(0, 0, width, height)

    for i, slot_size in enumerate(slot_sizes):
        base -= translate(
            box(0, 0, slot_size, slot_height),
            slot_interval * (i + 1),
            height - slot_height,
        )

    return base


model.add_model(hole_size_test())

model.add_part(
    fit_test_a(),
    translate=(0, 30, 0),
)

top_level_geom = model.render_full()

model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
