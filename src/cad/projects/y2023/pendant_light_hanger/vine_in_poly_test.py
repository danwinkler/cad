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


# random.seed(0)

model = MultipartModel()


@dataclass
class VineMakerLineString:
    geom: LineString

    def get_point(self, idx):
        return self.geom.coords[idx]

    def add_point(self, point):
        self.geom = LineString(list(self.geom.coords) + [point])


@dataclass
class VineMakerTip:
    line_string: VineMakerLineString
    segments_since_last_split: int
    rot: float


class VineMaker:
    def __init__(
        self, container: Polygon, start_pos: euclid3.Vector2, start_vec: euclid3.Vector2
    ):
        self.container = container
        self.pos = start_pos
        self.vec = start_vec
        self.line_strings = []
        self.tips = []

    def create(self):
        start = VineMakerLineString(LineString([self.pos.copy(), self.pos + self.vec]))
        self.line_strings.append(start)
        self.tips.append(VineMakerTip(start, 0, 0))

        i = 0
        while self.tips:
            tip = self.tips.pop(0)
            self.extend_tip(tip)

            if i > 2000:
                break

            if i % 250 == 0:
                print(i)

            i += 1

    def extend_tip(self, tip):
        last_vec = euclid3.Vector2(*tip.line_string.get_point(-1)) - euclid3.Vector2(
            *tip.line_string.get_point(-2)
        )
        last_angle = math.atan2(last_vec.y, last_vec.x)
        rot = tip.rot + random.uniform(-0.1, 0.1)
        max_rot = 0.3
        rot = max(-max_rot, min(max_rot, rot))

        new_angle = last_angle + rot
        new_vec = euclid3.Vector2(math.cos(new_angle), math.sin(new_angle))
        new_vec *= last_vec.magnitude()
        new_pos = tip.line_string.get_point(-1) + new_vec

        segments_since_last_split = tip.segments_since_last_split + 1

        split = tip.segments_since_last_split > 2  # and random.random() < 0.5

        if split:
            segments_since_last_split = 0

        self.add_tip(
            tip.line_string,
            tip.line_string.get_point(-1),
            new_pos,
            segments_since_last_split,
            rot,
        )

        if split:
            segments_since_last_split = 0
            side = random.choice([-1, 1])
            split_angle = last_angle + side * random.uniform(0.3, 1.5)
            split_vec = euclid3.Vector2(math.cos(split_angle), math.sin(split_angle))
            split_vec *= last_vec.magnitude()
            split_pos = tip.line_string.get_point(-1) + split_vec

            self.add_tip(None, tip.line_string.get_point(-1), split_pos, 0, 0)

    def add_tip(self, line_string, last_point, point, segments_since_last_split, rot):
        # Check that the line doesn't intersect any previous line
        line_seg = LineString([last_point, point])

        for l_seg in self.line_strings:
            intersection = l_seg.geom.intersection(line_seg)
            if intersection.geom_type == "Point":
                # If the intersection is at the beginning of the line, that's okay

                if intersection.distance(Point(last_point)) < 0.1:
                    continue

                if line_string is not None:
                    line_string.add_point(intersection.coords[0])

                return

        # If the point isn't in the container, return
        if not self.container.contains(Point(point)):
            # Try to find the intersection with the container (this can fail)
            exterior_ls = LineString(self.container.exterior.coords)
            intersection = exterior_ls.intersection(line_seg)
            if intersection.geom_type == "Point":
                if line_string is not None:
                    line_string.add_point(intersection.coords[0])

            return

        if line_string is None:
            line_string = VineMakerLineString(line_seg)
            self.line_strings.append(line_string)
        else:
            line_string.add_point(point)

        self.tips.append(VineMakerTip(line_string, segments_since_last_split, rot))


def test():
    m = Model()

    vm = VineMaker(
        box(0, 0, 100, 100),
        euclid3.Vector2(50, 0),
        euclid3.Vector2(0, 2),
    )

    vm.create()

    skeleton = []
    for ls in vm.line_strings:
        for i in range(len(ls.geom.coords) - 1):
            a = ls.geom.coords[i]
            b = ls.geom.coords[i + 1]
            skeleton += [((a[0], a[1], 1000), (b[0], b[1], 1000))]

    for i in range(len(vm.container.exterior.coords)):
        a = vm.container.exterior.coords[i]
        b = vm.container.exterior.coords[(i + 1) % len(vm.container.exterior.coords)]
        skeleton += [((a[0], a[1], 1000), (b[0], b[1], 1000))]

    polys = skeleton_to_polys(
        skeleton, im_scale=5.0, blur=5, margin=5, threshold=30, debug_image=False
    )

    m.add_poly(unary_union(polys))

    return m


model.add_model(
    test(),
)

top_level_geom = model.render_full()

model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
