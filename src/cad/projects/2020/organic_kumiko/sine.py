import math
import random

import pyclipper
from solid import *
from solid.utils import *

from cad.common.helper import *


class Piece:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.connections = []


class Kumiko:
    def __init__(self):
        self.pieces = []

    def get_part(self):
        pass


parts = []


def position_fn(index, offset=Vec3()):
    return Vec3(index * 20, math.sin(index * 0.7) * 30, 0) + offset


k = Kumiko()

# parts.append(kumiko.get_part())


def make_poly(verts):
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        pyclipper.scale_to_clipper([[v.x, v.y] for v in verts]),
        pyclipper.JT_SQUARE,
        pyclipper.ET_CLOSEDLINE,
    )

    p2 = pyclipper.scale_from_clipper(pco.Execute(pyclipper.scale_to_clipper(1)))
    part = linear_extrude(height=10)(polygon(points=p2[0])) - down(1)(
        linear_extrude(height=12)(polygon(points=p2[1]))
    )

    parts.append(part)


lines = [
    # Bottom
    [position_fn(i) for i in range(20)],
    # Top
    [position_fn(i, offset=Vec3(0, 20, 0)) for i in range(20)],
    [
        position_fn(i // 2, offset=Vec3(0, 20, 0) if i % 2 else Vec3())
        for i in range(40)
    ],
]

"""
for line in lines:
    pco = pyclipper.PyclipperOffset()
    pco.AddPath( pyclipper.scale_to_clipper( [[v.x, v.y] for v in line] ), pyclipper.JT_SQUARE, pyclipper.ET_OPENSQUARE )

    p2 = pyclipper.scale_from_clipper( pco.Execute( pyclipper.scale_to_clipper( 1 ) ) )
    
    part = union() ( [down( 1 ) ( linear_extrude( height=10 ) (
        polygon( points=path )
    )) for path in p2] )

    parts.append(part)
"""

for i in range(20):
    zero_offset = Vec3()
    adjacent_offset = Vec3(0, 20, 0)
    p0 = position_fn(i)
    p1 = position_fn(i, offset=adjacent_offset)
    p2 = position_fn(i + 1)
    p3 = position_fn(i + 1, offset=adjacent_offset)

    make_poly([p0, p1, p2])
    make_poly([p1, p2, p3])


print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
