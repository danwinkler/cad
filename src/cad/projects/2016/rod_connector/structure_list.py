from structure_class import *
import math
import random
import noise


class S1(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 30) + (150 if a % 2 == 0 else -100)
        return angle, dist


class S2(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 30) + math.cos(angle_minus_offset * 2) * 150
        return angle, dist


class S3(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 30) + math.cos(angle_minus_offset) * 200
        return angle, dist


class S4(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 30) - math.cos(angle_minus_offset * 2) * 150
        return angle, dist


class S5(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        height = float(h) / float(self.height)
        height *= math.pi
        dist = 500 - math.sin(height) * 250 + h ** 3 * 0.6
        return angle, dist


class S6(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 30) + (100 if a % 3 == 0 else 0)
        hscale = 300
        return angle, dist


class S7(LayerStructure):
    hscale = 300
    height = 10
    sections = 6

    def calc(self, h, a):
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / self.sections) * a
        angle = angle_minus_offset + offset * h
        dist = 500 - abs(h) * 30
        return angle, dist


class RandS1(RandomMeshStructure):
    seed = 1
    min_point_dist = 1000
    height = 3000
    avg_rad = 500

    def calc(self, x, y):
        a = x * math.pi
        h = y * 10
        offset = math.pi * 0.125
        angle_minus_offset = (math.pi * 2 / 6) * a
        angle = angle_minus_offset + offset * h
        dist = (500 - h * 40) + math.sin(y * 20 + x * 20) * 60 + 50
        return dist


class WP1(WallPiece):
    width = 1000
    height = 1000
    seed = 2
    # seed = 19523195
    point_count = 50

    random.seed(seed)
    points = [
        Vec3(random.uniform(0, 1000), random.uniform(0, 1000), random.uniform(0, 100))
        for i in range(point_count)
    ]
    points += [Vec3(0, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 0, 0) for i in range(11)]
    points += [Vec3(1000, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 1000, 0) for i in range(11)]

    sx_points = range(point_count, point_count + 11)
    sy_points = range(point_count + 11, point_count + 22)
    bx_points = range(point_count + 22, point_count + 33)
    by_points = range(point_count + 33, point_count + 44)


class WP2(WallPiece):
    width = 1000
    height = 1000
    # seed = 2
    seed = 195231
    point_count = 64

    def height_func(x, y):
        return (noise.snoise2(x * 0.003 + y * 0.03, y * 0.003) + 1) * 50

    random.seed(seed)
    # points = [Vec3(random.uniform(50, 950), random.uniform(50, 950), random.uniform(0, 100)) for i in range(point_count)]
    points = [
        Vec3(
            i % 8 * (1000 / 8.0) + (1000 / 16.0),
            i / 8 * (1000 / 8.0) + (1000 / 16.0),
            random.uniform(0, 100),
        )
        for i in range(point_count)
    ]

    for p in points:
        p.z = min(max(height_func(p.x, p.y), 0), 100)

    points += [Vec3(0, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 0, 0) for i in range(11)]
    points += [Vec3(1000, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 1000, 0) for i in range(11)]

    sx_points = range(point_count, point_count + 11)
    sy_points = range(point_count + 11, point_count + 22)
    bx_points = range(point_count + 22, point_count + 33)
    by_points = range(point_count + 33, point_count + 44)


class WP3(WallPiece):
    width = 1219.2
    height = 1219.2
    inc = width / 10
    seed = 2
    # seed = 19523195
    min_dist = width * 0.13

    def height_func(x, y):
        return 30 + (noise.snoise2(x * 0.005, y * 0.005) + 1) * 80

    random.seed(seed)
    points = []
    while True:
        placed = False
        for i in xrange(10000):
            p = Vec3(
                random.uniform(inc * 0.5, width - inc * 0.5),
                random.uniform(inc * 0.5, width - inc * 0.5),
                random.uniform(30, 100),
            )
            good = True
            for o in points:
                if o.distance2(p) < min_dist ** 2:
                    good = False
                    break

            if good:
                points.append(p)

        if not placed:
            break

    for p in points:
        p.z = height_func(p.x, p.y)

    point_count = len(points)
    points += [Vec3(0, i * inc, 0) for i in range(11)]
    points += [Vec3(i * inc, 0, 0) for i in range(11)]
    points += [Vec3(width, i * inc, 0) for i in range(11)]
    points += [Vec3(i * inc, height, 0) for i in range(11)]

    sx_points = range(point_count, point_count + 11)
    sy_points = range(point_count + 11, point_count + 22)
    bx_points = range(point_count + 22, point_count + 33)
    by_points = range(point_count + 33, point_count + 44)


class WP4(WallPiece):
    width = 1000
    height = 1000
    seed = 2
    # seed = 19523195
    min_dist = 130

    random.seed(seed)
    points = []
    while True:
        placed = False
        for i in xrange(10000):
            p = Vec3(
                random.uniform(50, 950), random.uniform(50, 950), random.uniform(0, 100)
            )
            good = True
            for o in points:
                if o.distance2(p) < min_dist ** 2:
                    good = False
                    break

            if good:
                points.append(p)

        if not placed:
            break

    point_count = len(points)
    points += [Vec3(0, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 0, 0) for i in range(11)]
    points += [Vec3(1000, i * 100, 0) for i in range(11)]
    points += [Vec3(i * 100, 1000, 0) for i in range(11)]

    sx_points = range(point_count, point_count + 11)
    sy_points = range(point_count + 11, point_count + 22)
    bx_points = range(point_count + 22, point_count + 33)
    by_points = range(point_count + 33, point_count + 44)
