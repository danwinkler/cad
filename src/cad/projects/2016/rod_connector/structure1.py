import math
import random
import time

from solid import *
from solid.utils import *

from cad.common.helper import *

from . import connector as conn
from . import layer_structure

layer_count = 10
rot_count = 6
offset = math.pi * 0.125

layers = []

# Create points
for h in range(layer_count):
    layer = []
    for a in range(rot_count):
        angle_minus_offset = (math.pi * 2 / rot_count) * a
        angle = angle_minus_offset + offset * h

        dist = (500 - h * 30) + (150 if a % 2 == 0 else -100)  # Variation E

        if False and h < 4 and h > 0 and a == 0:
            layer.append(None)
        else:
            layer.append(Vec3(math.cos(angle) * dist, math.sin(angle) * dist, h * 300))
    layers.append(layer)

parts = layer_structure.create_from_layers(layers, save_name="varE")
layer_structure.create_from_layers_stick_list(layers, save_name="varE")
layer_structure.create_vase(layers, save_name="varE")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
