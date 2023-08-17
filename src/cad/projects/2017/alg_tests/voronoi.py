import math
import random
import sys

from scipy.spatial import Voronoi
from solid import *
from solid.utils import *

from cad.common.helper import *

points = [[random.uniform(0, 10), random.uniform(0, 10)] for i in range(100)]

vor = Voronoi(points)

# Remove incomplete regions
regions = filter(lambda x: all(i >= 0 for i in x) and len(x) > 0, vor.regions)

# Assemble extruded sections
parts = []
for region in regions:
    h = random.uniform(0.5, 1.5)

    verts = [vor.vertices[r] for r in region]
    parts.append(
        linear_extrude(height=h)(polygon(points=[[v[0], v[1]] for v in verts]))
    )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
