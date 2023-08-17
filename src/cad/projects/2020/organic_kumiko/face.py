import math
import random
from collections import defaultdict

import networkx
import pyclipper
from solid import *
from solid.utils import *

from cad.common.helper import *


def make_poly(verts, offset=1):
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        pyclipper.scale_to_clipper([[v.x, v.y] for v in verts]),
        pyclipper.JT_SQUARE,
        pyclipper.ET_CLOSEDPOLYGON,
    )

    p2 = pyclipper.scale_from_clipper(pco.Execute(pyclipper.scale_to_clipper(-offset)))
    return union()([polygon(points=points) for points in p2])


class GridStore:
    def __init__(self):
        self.points = defaultdict(list)
        self.connections = []

    def put(self, a, b):
        self.points[a].append(b)
        self.points[b].append(a)
        self.connections.append(Line(a, b))

    def get_chordless_cycles(self):
        points_list = self.points.keys()
        point_to_index = {p: i for i, p in enumerate(points_list)}

        graph = networkx.Graph()
        for connection in self.connections:
            graph.add_edge(connection.a, connection.b)

        is_planar, planar_emb = networkx.check_planarity(graph)

        if not is_planar:
            raise Exception("Not planar")

        node_to_neighbors = planar_emb.get_data()

        half_edges = set()

        faces = []
        for node, neighbors in node_to_neighbors.items():
            for neighbor in neighbors:
                if (node, neighbor) not in half_edges:
                    faces.append(planar_emb.traverse_face(node, neighbor, half_edges))

        return faces


DEPTH = 10
WIDTH = 100
THICKNESS = 2
W2 = WIDTH / 2

holes = []
block = cube([WIDTH + THICKNESS, WIDTH + THICKNESS, 10])

grid = GridStore()

for i in range(4):
    # 90deg from center
    t = math.pi * 0.5

    angle = t * i

    center = Vec3(W2, W2, 0)
    out = center + Vec3(math.cos(angle) * W2, math.sin(angle) * W2, 0)
    right = out + Vec3(math.cos(angle + t) * W2, math.sin(angle + t) * W2, 0)
    left = out + Vec3(math.cos(angle - t) * W2, math.sin(angle - t) * W2, 0)

    mid_t = math.pi * 0.2
    mid_d = W2 * 0.3

    mid_a = (center + right + out) * (1.0 / 3.0)
    mid_b = (center + left + out) * (1.0 / 3.0)

    center.round()
    out.round()
    right.round()
    left.round()
    mid_a.round()
    mid_b.round()

    grid.put(center, out)
    grid.put(out, right)
    grid.put(right, center)
    grid.put(out, left)
    grid.put(center, mid_a)
    grid.put(out, mid_a)
    grid.put(right, mid_a)

    grid.put(center, mid_b)
    grid.put(out, mid_b)
    grid.put(left, mid_b)

cycles = grid.get_chordless_cycles()

cycles = [c for c in cycles if len(c) == 3]

parts = []

holes += [linear_extrude(height=DEPTH + 2)(make_poly(cycle)) for cycle in cycles]

parts.append(block - translate([THICKNESS / 2, THICKNESS / 2, -1])(holes))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
