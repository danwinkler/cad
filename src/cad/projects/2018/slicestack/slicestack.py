import copy
import math
import random
import platform
import os
from pathlib import Path

from solid import *
from solid.utils import *
from tqdm import tqdm
from plumbum import local
import pyclipper
from scipy.interpolate import splprep, splev
from scipy.optimize import fmin
from scipy.spatial.distance import euclidean
import numpy as np

from dan.lib.helper import *
from dan.lib import polytri
from dan.project.slicestack.differential_line import DiffLine, NodeData

df = DiffLine()
df.init_circle()

layers = []
points_per_layer = 300
height = 200
flip = False

print("Running Simulation")
for i in tqdm(range(height)):
    df.update()

    if i % 20 == 0:
        layer = []
        for n in df.nodes:
            nd = NodeData(n)
            if flip:
                nd.pos.z = height - i
            else:
                nd.pos.z = i
            layer.append(nd)
        layers.append(layer)

parts = []

def convert_points_to_spline(points):
    arr = np.array([p.to_list() for p in points])
    tck, u = splprep(arr.T, s=0.0, per=1, quiet=2)
    return tck, u

def normalize_points_on_layer(layer, num_points=points_per_layer):
    z = layer[0].z
    arr = np.array([(p.x, p.y) for p in layer])
    tck, u = splprep(arr.T, u=None, s=0.0, per=1, quiet=2)
    u_new = np.linspace(u.min(), u.max(), points_per_layer)
    x_new, y_new = splev(u_new, tck, der=0)
    return [
        Vec3(x, y_new[i], z) for i, x in enumerate(x_new)
    ]


def shrink_layer(layer, offset):
    z = layer[0].z

    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        [(p.x, p.y) for p in layer],
        pyclipper.JT_SQUARE,
        pyclipper.ET_CLOSEDPOLYGON
    )

    solution = pco.Execute(-offset)

    if len(solution) > 1:
        print( "warning, solution len: {}".format(len(solution)))

    # Only use the longest solution, if there's more than one we're probably fucked anyhow
    path = max(solution, key=lambda d: len(d))

    return [Vec3(p[0], p[1], z) for p in path]


def sample_closest_points(layers, num_points):
    ret_layers = []

    # sample first layer
    ret_layers.append(normalize_points_on_layer(layers[0], num_points))

    for layer_index, layer in tqdm(enumerate(layers), total=len(layers)):
        if layer_index == 0:
            continue

        previous_layer = ret_layers[layer_index-1]

        # Rotate layer
        layer = deque(layer)
        closest_index, closest_point = min(enumerate(layer), key=lambda ip: ip[1].distance(previous_layer[0]))
        layer.rotate(-closest_index)
        layer = list(layer)
        
        new_layer = []

        index_ratio = len(layer) / len(previous_layer)

        p_index = 0
        for bp in previous_layer:
            try:
                #closest_index, closest_point = min(enumerate(layer[p_index:p_index+int(index_ratio*1)]), key=lambda ip: ip[1].distance2(bp))
                closest_index, closest_point = min(enumerate(layer), key=lambda ip: Vec3(ip[1].x, ip[1].y).distance2(Vec3(bp.x, bp.y)))
            except ValueError:
                new_layer.append(layer[0])
            else:
                # we cut off the beginning of the layer array so have to add this value back
                closest_index += p_index
                p_index = closest_index+1

                new_layer.append(closest_point)

        ret_layers.append(new_layer)

    
    return ret_layers

def normalize_stack(layers, num_points):
    ret_layers = []

    ret_layers.append(normalize_points_on_layer(layers[0], num_points))

    def dist_to_point_function(p, tck):
        def dist_to_p(u):
            s = splev(u, tck)
            return euclidean(p, s)

    for layer in enumerate(layers[1:]):
        pass

def insert_points_in_long_sections(layer, max_length=5.0):
    out = []
    for i, p in enumerate(layer):
        out.append(p)
        next_point = layer[(i+1)%len(layer)]
        vec = next_point - p
        dist = vec.length()
        usable_dist = dist - 1
        if usable_dist > max_length:
            # Normalize
            vec /= dist
            vec *= max_length
            for _ in range(int(usable_dist / max_length)):
                out.append(out[-1] + vec)
    return out

shrink_amount = 3

# Convert to just pos
layers = [[nd.pos for nd in layer] for layer in layers]

print("Smoothing")
# layers = [normalize_points_on_layer(layer, len(layer)*2) for layer in layers]

print("Resizing")
og_layers = layers
layers = [shrink_layer(layer, 0) for layer in og_layers]
shrunk_layers = [shrink_layer(layer, 5) for layer in og_layers]

print("Filling long spans")
layers = [insert_points_in_long_sections(layer) for layer in layers]
shrunk_layers = [insert_points_in_long_sections(layer) for layer in shrunk_layers]

# for layer in layers:
#     for p in layer:
#         parts.append(translate(p.to_list())(cube([1,1,1])))

print("Normalizing")
layers = [normalize_points_on_layer(layer) for layer in layers]
shrunk_layers = [normalize_points_on_layer(layer) for layer in shrunk_layers]

#layers = sample_closest_points(layers, 300)
#shrunk_layers = sample_closest_points(shrunk_layers, 300)

print( "Triangulating" )
#outer = rings_to_polyhedron(layers[:-1], progress_stdout=True)
#inner = rings_to_polyhedron(shrunk_layers[1:], progress_stdout=True)
outer = similar_rings_to_polyhedron(layers[:-1], progress_stdout=True)
inner = similar_rings_to_polyhedron(shrunk_layers[1:], progress_stdout=True)

#parts.append( outer )
#parts.append( inner )
parts.append(outer - inner)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
