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
    BendyRenderer,
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)


class BoxA:
    def __init__(self):
        self.kerf_adjustment = 0.11
        self.tab_width = 10
        self.width = 80
        self.length = 160
        self.depth = 40
        self.wood_thickness = 4.9
        self.lid_lip_offset = 15

    def joint_cut(self, start, end, offset=False):
        cuts = []
        x = start + self.tab_width if offset else start
        while x < end:
            start_adjustment = self.kerf_adjustment if x > start else 0
            end_adjustment = self.kerf_adjustment if x < end - self.tab_width else 0
            cuts.append(
                box(
                    x + start_adjustment,
                    0,
                    x + self.tab_width - end_adjustment,
                    self.wood_thickness,
                )
            )
            x += self.tab_width * 2

        return unary_union(cuts)

    def text(self, text, scale=0.002):
        lines = text.split("\n")
        polys = [
            scale(get_text_polygon(line), scale, scale, origin=(0, 0)) for line in lines
        ]

        arranged_polys = []
        y = 0
        for poly in polys:
            arranged_polys.append(translate(poly, 0, y))
            y += (poly.bounds[3] - poly.bounds[1]) * 1.2

        return unary_union(arranged_polys)

    def side(self, x_dim, y_dim, bottom, right, top, left):
        shape = box(0, 0, x_dim, y_dim)

        if bottom:
            shape = shape.difference(self.joint_cut(0, x_dim, offset=bottom == 2))

        if right:
            shape = shape.difference(
                translate(
                    rotate(
                        self.joint_cut(0, y_dim, offset=right == 2), 90, origin=(0, 0)
                    ),
                    x_dim,
                    0,
                )
            )

        if top:
            shape = shape.difference(
                translate(
                    rotate(
                        self.joint_cut(0, x_dim, offset=top == 2), 180, origin=(0, 0)
                    ),
                    x_dim,
                    y_dim,
                )
            )
        if left:
            shape = shape.difference(
                translate(
                    rotate(
                        self.joint_cut(0, y_dim, offset=left == 2), 270, origin=(0, 0)
                    ),
                    0,
                    y_dim,
                )
            )

        return shape

    def lip_lid_cutout(self, width):
        return box(
            self.lid_lip_offset,
            self.depth - self.wood_thickness,
            width - self.lid_lip_offset,
            self.depth,
        )

    def bottom(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.width, self.length, 1, 1, 1, 1)
        m.add_poly(shape)
        return m

    def front(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.width, self.depth, 2, 1, 0, 1)
        shape -= self.lip_lid_cutout(self.width)
        m.add_poly(shape)
        return m

    def right(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.length, self.depth, 2, 1, 0, 1)
        shape -= self.lip_lid_cutout(self.length)
        m.add_poly(shape)
        return m

    def back(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.width, self.depth, 2, 1, 0, 1)
        shape -= self.lip_lid_cutout(self.width)
        m.add_poly(shape)
        return m

    def left(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.length, self.depth, 2, 1, 0, 1)
        shape -= self.lip_lid_cutout(self.length)
        m.add_poly(shape)
        return m

    def lid(self):
        m = Model(thickness=self.wood_thickness)
        shape = unary_union(
            [
                box(
                    self.wood_thickness,
                    self.wood_thickness,
                    self.width - self.wood_thickness,
                    self.length - self.wood_thickness,
                ),
                box(
                    0,
                    self.lid_lip_offset,
                    self.width,
                    self.length - self.lid_lip_offset,
                ),
                box(
                    self.lid_lip_offset,
                    0,
                    self.width - self.lid_lip_offset,
                    self.length,
                ),
            ]
        )
        m.add_poly(shape)
        return m

    def get_model(self):
        """
        The current implementation needs all sides to be an even multiple of tab_width*2
        """

        assert self.width % (self.tab_width * 2) == 0
        assert self.length % (self.tab_width * 2) == 0
        assert self.depth % (self.tab_width * 2) == 0

        col_a = (0.8, 0.5, 0.2)
        col_b = (0.7, 0.4, 0.1)

        m = MultipartModel(self.wood_thickness)

        m.add_model(self.bottom())
        m.add_model(self.front()).renderer.rotate(90, [1, 0, 0]).translate(
            y=self.wood_thickness
        ).color(*col_a)
        m.add_model(self.right()).renderer.rotate(90, [1, 0, 0]).rotate(
            90, [0, 0, 1]
        ).translate(self.width - self.wood_thickness).color(*col_b)
        m.add_model(self.back()).renderer.rotate(90, [1, 0, 0]).rotate(
            180, [0, 0, 1]
        ).translate(self.width, self.length - self.wood_thickness).color(*col_a)
        m.add_model(self.left()).renderer.rotate(90, [1, 0, 0]).rotate(
            270, [0, 0, 1]
        ).translate(self.wood_thickness, self.length).color(*col_b)
        m.add_model(self.lid()).renderer.translate(z=self.depth - self.wood_thickness)

        return m


box_inst = BoxA()
box_inst.depth = 80
box_inst.width = 100
box_inst.length = 200

model = box_inst.get_model()

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
model.render_parts(output_dir)
model.render_single_dxf(output_dir / "single.dxf")

top_level_geom = model.render_scad()

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
