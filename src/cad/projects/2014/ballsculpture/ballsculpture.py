import math
import random
import sys

from solid import *
from solid.utils import *

from cad.common.helper import Vec3

balls = []

balls.append([Vec3(0, 0, 0), 20])

height = 50

while True:
    lb = balls[random.randint(0, len(balls) - 1)]
    v = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(1, 1))
    vl = v.length()
    s = random.uniform(5, 20)

    sep = 3

    v.normalize()
    v *= lb[1] + s - sep

    v += lb[0]

    if v.z > height:
        continue

    good = True
    for ball in balls:
        if v.distance(ball[0]) < (ball[1] + s - sep):
            good = False
            break

    if good:
        balls.append([v, s])
        print("added " + str(len(balls)))

    if len(balls) >= 70:
        break

parts = []

neg_parts = []

neg_parts.append(translate([0, 0, -500])(cube([1000, 1000, 1000])))

for ball in balls:
    ball[0].z = height - ball[0].z
    tlist = ball[0].to_list()
    parts.append(
        translate(tlist)(sphere(ball[1]))
    )  # , segments=int(ball[1]*.5)+9 ) ) )
    # neg_parts.append( translate( ball[0].to_list() ) ( sphere( ball[1]-2 ) ) )

parts = difference()(union()(parts), union()(neg_parts))

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
