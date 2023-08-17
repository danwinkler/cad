import math
import random

from scipy.spatial import Voronoi

from cad.common.helper import *

random.seed(0)

x_size = 100
y_size = 100
z_min = -50
z_size = 100


num_points = 100
min_dist = 5
min_dist2 = min_dist**2

r = 1


points = []

print("Create points")
while len(points) < num_points:
    p = Vec3(
        random.uniform(0, x_size),
        random.uniform(0, y_size),
        random.uniform(z_min, z_size),
    )
    if all(op.distance2(p) > min_dist2 for op in points):
        points.append(p)

for i in range(100):
    p = Vec3(
        random.uniform(0, x_size), random.uniform(0, y_size), random.uniform(z_min, 0)
    )
    if all(op.distance2(p) > min_dist2 for op in points):
        points.append(p)

print("Voronoi")
vor = Voronoi([p.to_list() for p in points])

print("Assemble point/ridge objects")


class PointObj:
    def __init__(self, p):
        self.ridges = []
        self.p = p


class RidgeObj:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def other(self, p):
        if p is self.p0:
            return self.p1
        return self.p0


point_list = [PointObj(Vec3(v[0], v[1], v[2])) for v in vor.vertices]
ridge_log = {}
ridge_list = []

for ridge in vor.ridge_vertices:
    if ridge[0] == -1 or ridge[1] == -1:
        continue

    for i in range(len(ridge) - 1):
        p0 = point_list[ridge[i]]
        p1 = point_list[ridge[i + 1]]

        s0 = str(ridge[i]) + "-" + str(ridge[i + 1])
        s1 = str(ridge[i + 1]) + "-" + str(ridge[i])

        if s0 in ridge_log or s1 in ridge_log:
            continue

        ridge_log[s0] = True
        ro = RidgeObj(p0, p1)
        ridge_list.append(ro)
        p0.ridges.append(ro)
        p1.ridges.append(ro)

print("Culling unwanted points and ridges")
while True:
    removed_points = 0

    for p in point_list:
        remove = False

        v = p.p
        if (
            v.x < 0
            or v.x > x_size
            or v.y < 0
            or v.y > y_size
            or v.z < z_min
            or v.z > z_size
        ):
            remove = True

        if len(p.ridges) < 3:
            remove = True

        if remove:
            removed_points += 1
            point_list.remove(p)
            for ridge in p.ridges:
                ridge_list.remove(ridge)
                ridge.other(p).ridges.remove(ridge)

    print("cycle " + str(removed_points))
    if removed_points == 0:
        break

print("Final below ground point/ridge removal")
point_list = filter(lambda p: p.p.z > -r, point_list)
ridge_list = filter(lambda ro: ro.p0.p.z > -r or ro.p1.p.z > -r, ridge_list)
