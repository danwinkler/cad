import math
import random

import pyclipper
from scipy.spatial import Voronoi
from solid import *
from solid.utils import *

from cad.common.helper import *

random.seed(0)

points = []

width = 40
height = 10

min_dist = 0.8
min_dist2 = min_dist * min_dist

honeycomb_regions = 50

print("Building initial point set")
for i in range(honeycomb_regions):
    print(str(i) + " out of " + str(honeycomb_regions))

    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    axis = Vec3(0, 0, 1)
    angle = math.pi * random.uniform(0, 2)

    w = random.randint(15, 20)
    h = random.randint(8, 10)

    for y in range(h):
        for x in range(w):
            offset = 0 if y % 2 == 0 else 0.5
            offset -= 5
            p = Vec3(x + offset, y, 0)
            p = p.rotate(axis, angle)
            p.x += tx
            p.y += ty
            points = list(filter(lambda tp: tp.distance2(p) > min_dist2, points))
            points.append(p)

# Remove points too far out
points = filter(
    lambda p: p.x > -5 and p.y > -5 and p.x < width + 5 and p.y < height + 5, points
)

# Caculating Voronoi
vor = Voronoi([p.to_list()[:2] for p in points])

# Remove incomplete regions
regions = list(filter(lambda x: all(i >= 0 for i in x) and len(x) > 0, vor.regions))


def area(corners):
    n = len(corners)  # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


# Remove too big regions
regions = list(
    filter(lambda region: area([vor.vertices[r] for r in region]) < 3, regions)
)

# Assemble extruded sections
print("Building openscad file")

holes = []
for region in regions:
    verts = [vor.vertices[r] for r in region]
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(
        pyclipper.scale_to_clipper([[v[0], v[1]] for v in verts]),
        pyclipper.JT_MITER,
        pyclipper.ET_CLOSEDPOLYGON,
    )

    p2 = pyclipper.scale_from_clipper(pco.Execute(pyclipper.scale_to_clipper(-0.1)))
    cutout = union()(
        [down(1)(linear_extrude(height=h + 2)(polygon(points=path))) for path in p2]
    )

    holes.append(cutout)

# Add Frame
parts = cube([width, height, 1]) - holes
parts += cube([width, height, 1]) - translate([1, 1, -1])(
    cube([width - 2, height - 2, 3])
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
