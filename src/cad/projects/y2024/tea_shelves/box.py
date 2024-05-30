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

        # Determines the width of the tabs used to join the sides and the bottom
        self.tab_width = 10
        self.width = 80  # The width of the box (x dimension)
        self.length = 160  # The length of the box (y dimension)
        self.depth = 40  # The depth of the box (z dimension)
        self.wood_thickness = 4.9  # The thickness of the wood used to make the box

        self.has_bottom = True
        self.has_lid = True
        # The lid shape is sort of a "cross", where it fits on all sides.
        # This means that the corners of the box extend all the way up, but the sides are recessed to fit the lid.
        # This is the side of the extended corners
        self.lid_lip_offset = 15

        # The number of internal spaces to divide the box into
        # The number of dividers is segments - 1
        self.x_segments = 1
        self.y_segments = 1

        self.bottom_divider_tab_width = 10

    def joint_cut(
        self,
        start,
        end,
        offset=False,
        skip_positions=[],
        tab_width=None,
        start_offset=0,
    ):
        if skip_positions:
            print(start, end, offset, skip_positions)

        if tab_width is None:
            tab_width = self.tab_width

        skip_margin = 5

        def should_skip(x):
            for skip_pos in skip_positions:
                if (
                    skip_pos + self.wood_thickness >= x - skip_margin
                    and skip_pos <= x + tab_width + skip_margin
                ):
                    return True
            return False

        # Step 1: determine the tab locations
        tab_locations = []
        x = start + start_offset
        while x < end:
            if not should_skip(x):
                tab_locations.append(x)
            x += tab_width * 2

        # Step 2: create shapely polygons for each tab
        cuts = []
        for i, tab_loc in enumerate(tab_locations):
            # Since we inverse the shape in the offset case, we need to adjust the start and end points to account for the kerf
            if offset:
                start_adjustment = -self.kerf_adjustment if tab_loc > start else 0
                end_adjustment = (
                    -self.kerf_adjustment if tab_loc < end - tab_width else 0
                )
            else:
                start_adjustment = self.kerf_adjustment if tab_loc > start else 0
                end_adjustment = (
                    self.kerf_adjustment if tab_loc < end - tab_width else 0
                )

            cuts.append(
                box(
                    tab_loc + start_adjustment,
                    0,
                    tab_loc + tab_width - end_adjustment,
                    self.wood_thickness,
                )
            )
        shape = unary_union(cuts)

        # Step 3: invert if offset
        if offset:
            shape = box(start, 0, end, self.wood_thickness).difference(shape)

        return shape

        # cuts = []
        # x = start - tab_width if offset else start
        # while x <= end:
        #     # Check if we're near a skip position
        #     should_skip = False
        #     for skip_pos in skip_positions:
        #         if (
        #             skip_pos + self.wood_thickness >= x - skip_margin
        #             and skip_pos <= x + tab_width + skip_margin
        #         ):
        #             should_skip = True
        #             break

        #     if should_skip:
        #         if offset:
        #             cuts.append(
        #                 box(
        #                     x - tab_width - self.kerf_adjustment,
        #                     0,
        #                     x + tab_width * 2 + self.kerf_adjustment,
        #                     self.wood_thickness,
        #                 )
        #             )
        #     else:
        #         start_adjustment = self.kerf_adjustment if x > start else 0
        #         end_adjustment = self.kerf_adjustment if x < end - tab_width else 0
        #         cuts.append(
        #             box(
        #                 x + start_adjustment,
        #                 0,
        #                 x + tab_width - end_adjustment,
        #                 self.wood_thickness,
        #             )
        #         )
        #     x += tab_width * 2

        # return unary_union(cuts)

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

        if bottom and self.has_bottom:
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

        # Segment dividers tab slots
        for i in range(self.n_x_dividers):
            x_pos = self.x_divider_pos(i)
            shape -= translate(
                rotate(
                    self.joint_cut(
                        0,
                        self.length,
                        offset=False,
                        skip_positions=[
                            self.length - self.y_divider_pos(i)
                            for i in range(self.n_y_dividers)
                        ]
                        + [0, self.length],
                        tab_width=self.bottom_divider_tab_width,
                        start_offset=self.tab_width * 0.5,
                    ),
                    90,
                    origin=(0, 0),
                ),
                xoff=x_pos + self.wood_thickness,
            )

        for i in range(self.n_y_dividers):
            y_pos = self.y_divider_pos(i)
            print("bottom y divider", y_pos)
            shape -= translate(
                rotate(
                    self.joint_cut(
                        0,
                        self.width,
                        offset=False,
                        skip_positions=[
                            self.x_divider_pos(i) for i in range(self.n_x_dividers)
                        ]
                        + [0, self.width],
                        tab_width=self.bottom_divider_tab_width,
                        start_offset=self.tab_width * 0.5,
                    ),
                    0,
                    origin=(0, 0),
                ),
                yoff=y_pos - self.wood_thickness,
            )

        m.add_poly(shape)
        return m

    def front(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.width, self.depth, 2, 1, 0, 2)
        if self.has_lid:
            shape -= self.lip_lid_cutout(self.width)

        # Segment dividers tab slots
        for i in range(self.n_x_dividers):
            x_pos = self.width - self.x_divider_pos(i)
            shape -= translate(
                rotate(
                    self.joint_cut(0, self.depth - self.tab_width, offset=True),
                    90,
                    origin=(0, 0),
                ),
                xoff=x_pos,
            )

        m.add_poly(shape)
        return m

    def right(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.length, self.depth, 2, 2, 0, 1)
        if self.has_lid:
            shape -= self.lip_lid_cutout(self.length)

        # Segment dividers tab slots
        for i in range(self.n_y_dividers):
            x_pos = self.y_divider_pos(i)
            shape -= translate(
                rotate(
                    self.joint_cut(0, self.depth - self.tab_width, offset=True),
                    90,
                    origin=(0, 0),
                ),
                xoff=x_pos,
            )

        m.add_poly(shape)
        return m

    def back(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.width, self.depth, 2, 1, 0, 2)
        if self.has_lid:
            shape -= self.lip_lid_cutout(self.width)

        # Segment dividers tab slots
        for i in range(self.n_x_dividers):
            x_pos = self.width - self.x_divider_pos(i)
            shape -= translate(
                rotate(
                    self.joint_cut(0, self.depth - self.tab_width, offset=True),
                    90,
                    origin=(0, 0),
                ),
                xoff=x_pos,
            )

        m.add_poly(shape)
        return m

    def left(self):
        m = Model(thickness=self.wood_thickness)
        shape = self.side(self.length, self.depth, 2, 2, 0, 1)
        if self.has_lid:
            shape -= self.lip_lid_cutout(self.length)

        # Segment dividers tab slots
        for i in range(self.n_y_dividers):
            x_pos = self.y_divider_pos(i)
            shape -= translate(
                rotate(
                    self.joint_cut(0, self.depth - self.tab_width, offset=True),
                    90,
                    origin=(0, 0),
                ),
                xoff=x_pos,
            )

        m.add_poly(shape)
        return m

    def divider(self, x_dim, y_dim, axis):
        m = Model(thickness=self.wood_thickness)

        full_y_dim = y_dim
        if self.has_lid:
            full_y_dim -= self.wood_thickness

        shape = box(
            0,
            0,
            x_dim,
            full_y_dim,
        )

        # Left side tabs
        shape -= translate(
            rotate(
                self.joint_cut(0, y_dim, offset=False),
                90,
                origin=(0, 0),
            ),
            self.wood_thickness,
            0,
        )

        shape -= box(
            0,
            full_y_dim - self.tab_width * 1.5,
            self.wood_thickness,
            full_y_dim,
        )

        # Right side tabs
        shape -= translate(
            rotate(
                self.joint_cut(0, y_dim, offset=False),
                90,
                origin=(0, 0),
            ),
            x_dim,
            0,
        )
        shape -= box(
            x_dim - self.wood_thickness,
            full_y_dim
            - self.tab_width
            * 1.5,  # This 1.5 is a bit of a hack and covers up another bug
            x_dim,
            full_y_dim,
        )

        # Slots for other dividers
        if axis == "x":
            n_dividers = self.n_y_dividers
            divider_pos_fn = lambda i: x_dim - self.y_divider_pos(i)
            bottom = 0
            top = self.depth / 2
        elif axis == "y":
            n_dividers = self.n_x_dividers
            divider_pos_fn = self.x_divider_pos
            bottom = self.depth / 2
            top = self.depth

        for i in range(n_dividers):
            x_pos = divider_pos_fn(i)
            shape -= box(
                x_pos,
                bottom,
                x_pos + self.wood_thickness,
                top,
            )

        # Bottom
        if self.has_bottom:
            print("divider bottom", axis)
            shape -= self.joint_cut(
                0,
                x_dim,
                offset=True,
                skip_positions=[divider_pos_fn(i) for i in range(n_dividers)]
                + [0, x_dim],
                tab_width=self.bottom_divider_tab_width,
                start_offset=self.tab_width * 0.5,
            )

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

    @property
    def n_x_dividers(self):
        return self.x_segments - 1

    @property
    def x_segment_size(self):
        return (self.width - self.wood_thickness) / self.x_segments

    def x_divider_pos(self, i):
        return self.x_segment_size * (i + 1)

    @property
    def n_y_dividers(self):
        return self.y_segments - 1

    @property
    def y_segment_size(self):
        return (self.length - self.wood_thickness) / self.y_segments

    def y_divider_pos(self, i):
        return self.wood_thickness + self.y_segment_size * (i + 1)

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

        lifted_lid = True

        if self.has_bottom:
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

        if self.has_lid:
            m.add_model(self.lid()).renderer.translate(
                z=self.depth
                - self.wood_thickness
                + (self.depth * 1.5 if lifted_lid else 0)
            )

        for i in range(self.n_x_dividers):
            x_pos = self.x_divider_pos(i)
            m.add_model(
                self.divider(self.length, self.depth, axis="x")
            ).renderer.rotate(90, [1, 0, 0]).rotate(90, [0, 0, 1]).translate(
                x=x_pos
            ).color(
                *col_b
            )

        for i in range(self.n_y_dividers):
            y_pos = self.y_divider_pos(i)
            m.add_model(self.divider(self.width, self.depth, axis="y")).renderer.rotate(
                90, [1, 0, 0]
            ).translate(y=y_pos).color(*col_a)

        return m


if __name__ == "__main__":
    box_inst = BoxA()
    box_inst.depth = 60
    box_inst.width = 140
    box_inst.length = 120
    box_inst.x_segments = 3
    box_inst.y_segments = 2

    model = box_inst.get_model()

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
