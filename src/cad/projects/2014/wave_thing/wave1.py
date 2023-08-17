import math
import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

rings = []

height = 40
segs = 30

h_freq_scale = 0.1
a_freq_scale = 1

for i in range(height):
    ring = []
    for a in range(segs):
        ring.append(
            (
                noise(
                    i * h_freq_scale,
                    math.sin((float(a) / segs) * math.pi) * a_freq_scale,
                    5,
                )
                + 1
            )
            * 0.7
        )
    rings.append(ring)

h_scale = lambda h: (height + 1 - h) * 0.25 + 5
a_to_p = lambda a, v, h: [math.cos(a) * h_scale(h) * v, math.sin(a) * h_scale(h) * v, h]

for h in range(len(rings) - 1):
    ringa = rings[h]
    ringb = rings[h + 1]
    points = []
    print(h)
    for i in range(len(ringa)):
        print(ringa[i])
        points.append(a_to_p(i * ((math.pi * 2) / segs), ringa[i], h))
    for i in range(len(ringb)):
        points.append(a_to_p(i * ((math.pi * 2) / segs), ringb[i], h + 1))

    points.append([0, 0, h])
    points.append([0, 0, h + 1])

    path = []
    for i in range(len(ringa)):
        path.append([i, i + segs, (i + 1) % segs])
        path.append([i + segs, ((i + 1) % segs) + segs, (i + 1) % segs])

    for i in range(len(ringa)):
        path.append([segs * 2, i, (i + 1) % segs])
        path.append([i + segs, segs * 2 + 1, ((i + 1) % segs) + segs])
    parts.append(polyhedron(points=points, triangles=path))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
