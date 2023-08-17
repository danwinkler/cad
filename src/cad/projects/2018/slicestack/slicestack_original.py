import copy
import math
import os
import pickle
import platform
import random
from pathlib import Path

import numpy as np
import pyclipper
from scipy.interpolate import splev, splprep
from scipy.optimize import fmin
from scipy.spatial.distance import euclidean
from solid import *
from solid.utils import *
from tqdm import tqdm

from cad.common import polytri
from cad.common.helper import *

from .differential_line import DiffLine, NodeData

df = DiffLine()
df.init_circle()

layers = []
points_per_layer = 300
height = 700
flip = False
cache_file = Path("sim_{}.pickle".format(height))

if cache_file.exists():
    with open(cache_file, "rb") as f:
        layers = pickle.load(f)
else:
    print("Running Simulation")
    for i in tqdm(range(height)):
        df.update()

        if i % 20 == 0:
            layer = []
            for ring in df.rings:
                ring_layer = []
                for n in ring:
                    nd = NodeData(n)
                    if flip:
                        nd.pos.z = height - i
                    else:
                        nd.pos.z = i
                    ring_layer.append(nd)
                layer.append(ring_layer)
            layers.append(layer)
    with open(cache_file, "wb") as f:
        pickle.dump(layers, f)


parts = []


def build_object(layers):
    pb = PolyhedronBuilder()

    def build_layers(pb, layers):
        for z, layer in tqdm(enumerate(layers), total=len(layers)):
            if z + 1 == len(layers):
                break
            next_layer = layers[z + 1]
            ai = 0
            bi = 0
            while bi < len(next_layer):
                b0 = next_layer[bi]
                b1 = next_layer[(bi + 1) % len(next_layer)]
                a0 = layer[ai % len(layer)]
                a1 = layer[(ai + 1) % len(layer)]
                pb.triangle(*(b0.pos, a0.pos, b1.pos)[::-1])
                bi += 1
                if b0.id == a0.id:
                    ai += 1
                    pb.triangle(*(b1.pos, a0.pos, a1.pos)[::-1])

    build_layers(pb, layers)

    def triangulate_layer(layer, order=1):
        z = layer[0].pos.z
        points = [(p.pos.x, p.pos.y) for p in layer]
        tris = polytri.triangulate(points)
        for triangle in tris:
            pb.triangle(*[Vec3(p[0], p[1], z) for p in triangle][::order])

    triangulate_layer(layers[0], order=1)
    triangulate_layer(layers[-1], order=-1)
    return pb.build()


outer = build_object([r[1] for r in layers[:-1]])
inner = build_object([r[0] for r in layers[1:]])


# parts.append( outer )
# parts.append( inner )
parts.append(scale([1.7, 1.7, 0.4])(outer - inner))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
