import functools
import itertools
import math
import random
import sys
from fractions import Fraction

from scipy.spatial import Delaunay
from solid import *
from solid.utils import *

from cad.common.helper import *


class LayerStructure:
    def get_layers(self, shrink_offset=0):
        layers = []
        for h in range(self.height):
            layer = []
            for a in range(self.sections):
                angle, dist = self.calc(h, a)
                dist -= shrink_offset
                layer.append(
                    Vec3(math.cos(angle) * dist, math.sin(angle) * dist, h * 300)
                )
            layers.append(layer)
        return layers


class RandomMeshStructure:
    def torus_dist2(self, p1, p2, w, h):
        return (
            min(abs(p1.x - p2.x), w - abs(p1.x - p2.x)) ** 2
            + min(abs(p1.y - p2.y), h - abs(p1.y - p2.y)) ** 2
        )

    def get_object(self, shrink_offset=0, seed=None):
        if not seed:
            seed = self.seed
        if not seed:
            seed = 0
        random.seed(seed)

        width = self.avg_rad * 2 * math.pi
        points = []

        # Put points along top and bottom
        edge_count = int(math.floor(width / self.min_point_dist))
        edge_width = width / edge_count
        for i in range(edge_count):
            points.append(Vec3(edge_width * i, 0))
            points.append(Vec3(edge_width * i, self.height))

        edge_points = [i for i in range(len(points))]

        # Fill the area with points
        while True:
            found = False
            for i in range(1000):
                point = Vec3(random.uniform(0, width), random.uniform(0, self.height))
                collides = False
                for p in points:
                    if (
                        self.torus_dist2(point, p, width, self.height)
                        < self.min_point_dist**2
                    ):
                        collides = True
                        break

                if not collides:
                    points.append(point)
                    found = True
                    break

            if not found:
                break

        # Bin the points into veritcal columns
        dsects_count = 4
        dsects_inc = width / dsects_count
        dsects = [[] for i in range(dsects_count)]
        for p in points:
            slot = int(p.x / dsects_inc)
            dsects[slot].append(p)

        # Create the Delaunay areas
        dareas = []
        ref_lists = [{} for i in range(dsects_count)]
        for i in range(dsects_count):
            if i - 1 < 0:
                bindex = i - 1 + dsects_count
                before = dsects[bindex]
                before = [Vec3(p.x - width, p.y) for p in before]
            else:
                bindex = i - 1
                before = dsects[i - 1]

            if i + 1 >= dsects_count:
                aindex = i + 1 - dsects_count
                after = dsects[aindex]
                after = [Vec3(p.x + width, p.y) for p in after]
            else:
                aindex = i + 1
                after = dsects[i + 1]

            for j in range(len(before)):
                ref_lists[i][j] = (bindex, j, True)

            for j in range(len(dsects[i])):
                ref_lists[i][j + len(before)] = (i, j, False)

            for j in range(len(after)):
                ref_lists[i][j + len(dsects[i]) + len(before)] = (aindex, j, True)

            dareas.append(before + dsects[i] + after)

        # Calculate Tris
        tris = []
        for i in range(dsects_count):
            tris.append(
                Delaunay([p.to_list()[:2] for p in dareas[i]], qhull_options="QJ")
            )

        def find_index(i, p):
            if p in ref_lists[i]:
                l, li, fake = ref_lists[i][p]
                point = dsects[l][li]

            for cpi in range(len(points)):
                if point is points[cpi]:
                    return cpi, fake

        # Make list of real tris
        real_tris = []
        for i in range(dsects_count):
            for t in tris[i].simplices:
                a, af = find_index(i, t[0])
                b, bf = find_index(i, t[1])
                c, cf = find_index(i, t[2])
                if af and bf and cf:
                    continue
                if a in edge_points and b in edge_points and c in edge_points:
                    continue
                real_tris.append([c, b, a])

        # Remove duplicates
        real_tris.sort()
        real_tris = list(k for k, _ in itertools.groupby(real_tris))
        real_tris = filter(lambda x: None not in x, real_tris)

        def realp(point):
            dist = self.calc(point.x / width, point.y / self.height) - shrink_offset
            a = point.x / width * math.pi * 2
            return Vec3(math.cos(a) * dist, math.sin(a) * dist, point.y)

        real_points = [realp(p) for p in points]

        real_points.append(Vec3(0, 0, 0))
        real_points.append(Vec3(0, 0, self.height))

        for i in range(edge_count):
            real_tris.append(
                [len(real_points) - 2, i * 2, (i * 2 + 2) % (edge_count * 2)]
            )

            real_tris.append(
                [(i * 2 + 3) % (edge_count * 2), i * 2 + 1, len(real_points) - 1]
            )

        return polyhedron(points=[p.to_list() for p in real_points], faces=real_tris)


class WallPiece:
    def get_object(self):
        points = list(self.points)  # Shallow Copy
        tris = Delaunay([p.to_list()[:2] for p in points], qhull_options="Qt")
        tris = [[t[0], t[1], t[2]] for t in tris.simplices]
        tris = [list(reversed(l)) for l in tris]

        edge_count = {}
        for tri in tris:
            for i in range(3):
                a = tri[i]
                b = tri[(i + 1) % 3]
                key = (a, b)
                edge = edge_count.get(key)
                if edge == None:
                    key = (b, a)
                    edge = edge_count.get(key)

                if edge == None:
                    edge_count[key] = 1
                else:
                    edge_count[key] = edge_count[key] + 1

        edges = []
        for key, value in edge_count.iteritems():
            if value == 1:
                edges.append(key[0])
                edges.append(key[1])

        edges = list(set(edges))
        avg_point = functools.reduce(lambda x, i: x + points[i], edges, Vec3())
        avg_point /= len(edges)
        avg_point.z = 0

        def get_angle(a):
            x = a.x - avg_point.x
            y = a.y - avg_point.y
            return atan2(y, x)

        def sort_fun(a, b):
            return 1 if get_angle(points[a]) < get_angle(points[b]) else -1

        edges.sort(sort_fun)

        new_points = []
        for p in edges:
            np = points[p].copy()
            np.z = 0
            new_points.append(np)

        for i in range(len(new_points)):
            t1 = [edges[i], len(points) + i, len(points) + ((i + 1) % len(new_points))]
            t2 = [
                edges[i],
                len(points) + ((i + 1) % len(new_points)),
                edges[(i + 1) % len(new_points)],
            ]
            tris.append(t1)
            tris.append(t2)

        points += new_points

        points.append(avg_point)
        for i in range(len(new_points)):
            tris.append(
                list(
                    reversed(
                        [
                            len(points) - 1,
                            len(points) - 1 - len(new_points) + i,
                            len(points)
                            - 1
                            - len(new_points)
                            + ((i + 1) % len(new_points)),
                        ]
                    )
                )
            )

        # return union() ( [translate( points[v].to_list() ) ( linear_extrude( 10 ) ( text( str(i), size=100, valign="center", halign="center" ) ) ) for i, v in enumerate( edges ) ])
        return polyhedron(points=[p.to_list() for p in points], faces=tris)

    def get_list(self):
        sorted_points = sorted(self.points, lambda a, b: cmp(a.y, b.y))
        sorted_points = filter(lambda x: x.z != 0, sorted_points)
        out = ""
        in_in_mm = 0.0393701
        win = self.width * in_in_mm
        hin = self.height * in_in_mm
        for i in range(len(sorted_points)):
            p = sorted_points[i].copy()
            height_in_mm = p.z
            p *= in_in_mm

            def convert_to_fraction(v):
                main = int(v * 16) / 16
                fraction = Fraction(int(v * 16) / 16.0 - main)
                return str(main) + " " + str(fraction)

            top_left = ", ".join([convert_to_fraction(v) for v in p.to_list()[:-1]])
            bottom_right = Vec3(win - p.x, hin - p.y, p.z)
            bottom_right = ", ".join(
                [convert_to_fraction(v) for v in bottom_right.to_list()[:-1]]
            )

            line = [i] + [top_left, bottom_right, convert_to_fraction(p.z)]
            line = [str(e) for e in line]
            out += " || ".join(line) + "\n"
        return out
