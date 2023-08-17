import itertools
import math
import random
from collections import defaultdict, deque, namedtuple

from numpy import number
from solid import *
from solid.utils import *
from tqdm import tqdm

from cad.common import polytri

in_to_mm = 25.4


class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.set(x, y, z)

    def set(self, x=0, y=0, z=0):
        if x.__class__ == Vec3:
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def length(self):
        return math.sqrt(self.length2())

    def length2(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def lerp(self, b, t):
        v = Vec3(b)
        v -= self
        v *= t
        v += self

        return v

    def to_list(self):
        return [self.x, self.y, self.z]

    def distance(self, other):
        return math.sqrt(self.distance2(other))

    def copy(self):
        return Vec3(self.x, self.y, self.z)

    def distance2(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return x * x + y * y + z * z

    def normalize(self):
        len = self.length()
        if len == 0:
            return
        self /= len
        return self

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def rotate(self, axis, angle):
        axis = axis.copy().normalize()
        vnorm = self.copy().normalize()
        _parallel = axis.dot(self)
        parallel = axis * _parallel
        perp = self - parallel
        cross = self.cross(axis)
        result = parallel + cross * math.sin(-angle) + perp * math.cos(-angle)
        return result

    def cross(self, v):
        cross_x = self.y * v.z - v.y * self.z
        cross_y = self.z * v.x - v.z * self.x
        cross_z = self.x * v.y - v.x * self.y
        return Vec3(cross_x, cross_y, cross_z)

    def round(self, ndigits=None):
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.z = round(self.z, ndigits)

    def __add__(self, other):
        if isinstance(other, (list, tuple)):
            other = Vec3(*other)
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if isinstance(other, (list, tuple)):
            other = Vec3(*other)
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, (list, tuple)):
            other = Vec3(*other)

        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __iadd__(self, other):
        if isinstance(other, (list, tuple)):
            other = Vec3(*other)
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __imul__(self, val):
        self.x *= val
        self.y *= val
        self.z *= val
        return self

    def __itruediv__(self, val):
        self.x /= val
        self.y /= val
        self.z /= val
        return self

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise Exception("Invalid index to Vec3")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise Exception("Invalid index to Vec3")

    def __repr__(self):
        return "({}, {}, {})".format(*self.to_list())

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return (
            isinstance(other, Vec3)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )


class Line:
    def __init__(self, a, b):
        if b.x < a.x or (b.x == a.x and b.y < a.y):
            self.a, self.b = b, a
        else:
            self.a, self.b = a, b

    def __hash__(self):
        return hash(self.a) ^ hash(self.b)

    def __eq__(self, other):
        return isinstance(other, Line) and self.a == other.a and self.b == other.b

    def __repr__(self):
        return "({}, {})".format(self.a, self.b)

    def other(self, p):
        if self.p == self.a:
            return self.b
        elif self.p == self.b:
            return self.a
        else:
            raise Exception()


# Find distance from point p to line segment
def point_to_line_segment(p, l0, l1):
    v = l1 - l0
    w = p - l0

    c1 = w.dot(v)
    if c1 < 0:
        return p.distance(l0)

    c2 = v.dot(v)
    if c2 < c1:
        return p.distance(l1)

    b = c1 / c2
    pb = l0 + v * b
    return p.distance(pb)


# Find distance**2 from point p to line segment
def point_to_line_segment_2(p, l0, l1):
    v = l1 - l0
    w = p - l0

    c1 = w.dot(v)
    if c1 < 0:
        return p.distance2(l0)

    c2 = v.dot(v)
    if c2 < c1:
        return p.distance2(l1)

    b = c1 / c2
    pb = l0 + v * b
    return p.distance2(pb)


# http://www.wyrmtale.com/blog/2013/115/2d-line-intersection-in-c
def line_line_intersect_2d(ps1, pe1, ps2, pe2):
    # Get A,B,C of first line - points : ps1 to pe1
    A1 = pe1.y - ps1.y
    B1 = ps1.x - pe1.x
    C1 = A1 * ps1.x + B1 * ps1.y

    # Get A,B,C of second line - points : ps2 to pe2
    A2 = pe2.y - ps2.y
    B2 = ps2.x - pe2.x
    C2 = A2 * ps2.x + B2 * ps2.y

    # Get delta and check if the lines are parallel
    delta = A1 * B2 - A2 * B1
    if delta == 0:
        raise ArithmeticError("Lines are parallel")

        # now return the Vector2 intersection point
    return Vec3((B2 * C1 - B1 * C2) / delta, (A1 * C2 - A2 * C1) / delta)


def cyl_on_vec(v, r=1, segments=6):
    v = v.copy()
    length = v.length()
    v.normalize()
    up_vec = Vec3(0, 0, 1)
    cross = up_vec.cross(v)
    angle = math.acos(up_vec.dot(v))
    return rotate(a=math.degrees(angle), v=cross.to_list())(
        cylinder(h=length, r=r, segments=segments)
    )


def rot_on_vec(v, obj):
    v = v.copy()
    length = v.length()
    v.normalize()
    up_vec = Vec3(0.000001, 0.000001, 1)
    cross = up_vec.cross(v)
    angle = math.acos(up_vec.dot(v))
    return rotate(a=math.degrees(angle), v=cross.to_list())(obj)


# Given a list of points and a width function,
# generates a "vine" polyhedron using make_trunk
# points - a list of Vec3's
# wf - a function that returns the distance from the point,
#      given the point index and the angle
# sections - the number of points around the circle
def vine(points, wf, sections=8):
    global dan_helper_vine_cross

    dan_helper_vine_cross = None

    def tf(h, a):
        global dan_helper_vine_cross

        if h == 0:
            vec = points[1] - points[0]
        elif h == len(points) - 1:
            vec = points[-1] - points[-2]
        else:
            vec = (points[h] - points[h - 1]) + (points[h + 1] - points[h])

        vec.normalize()

        if dan_helper_vine_cross == None:
            if vec.z == 1:
                dan_helper_vine_cross = Vec3(1, 0, 0)
            else:
                dan_helper_vine_cross = Vec3(0, 0, 1)

        angle = (a / float(sections)) * math.pi * 2

        p = vec.cross(dan_helper_vine_cross)

        p = p.cross(vec)

        dan_helper_vine_cross = p
        dan_helper_vine_cross.normalize()

        p = p.rotate(vec, angle)

        width = wf(h, angle)

        return [
            points[h].x + p.x * width,
            points[h].y + p.y * width,
            points[h].z + p.z * width,
        ]

    return make_trunk(len(points), sections, tf, index=True)


# Returns a polyhedron based on a set of points
# height - number of rows of points
# sections - number of points around each row (in a circle)
# pf - a function, that when given a height and a section number, returns a list [x,y,z]
# index - When false, pf is called with height and sections as floats between 0...1
#         When true, calls pf with the index (0...n)
def make_trunk(height, sections, pf, index=False):
    def add_points(p1, p2):
        return [p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2]]

    def scale_point(p, s):
        return [p[0] * s, p[1] * s, p[2] * s]

    points = []
    triangles = []

    max = height * sections

    # generate points
    for h in range(height):
        for s in range(sections):
            if index:
                points.append(pf(h, s))
            else:
                points.append(pf(h / float(height - 1), s / float(sections)))

    for h in range(height - 1):
        h2 = h + 1
        for s in range(sections):
            s2 = (s + 1) % sections

            # c------d
            # |  \   |
            # |   \  |
            # a------b

            a = h * sections + s
            b = h * sections + s2
            c = h2 * sections + s
            d = h2 * sections + s2

            triangles.append([a, c, b])
            triangles.append([b, c, d])

    bottom_avg = [0, 0, 0]
    top_avg = [0, 0, 0]
    for s in range(sections):
        bottom_avg = add_points(bottom_avg, points[s])
        top_avg = add_points(top_avg, points[((height - 1) * sections) + s])

    bottom_avg = scale_point(bottom_avg, 1.0 / sections)
    top_avg = scale_point(top_avg, 1.0 / sections)

    points.append(bottom_avg)
    points.append(top_avg)

    for s in range(sections):
        s2 = (s + 1) % sections
        triangles.append([s2, max, s])
        triangles.append(
            [((height - 1) * sections) + s, max + 1, ((height - 1) * sections) + s2]
        )

    return polyhedron(points=points, faces=triangles)


def in_inches(fn):
    def wrapper(*args, **kwargs):
        return scale(in_to_mm)(fn(*args, **kwargs))

    return wrapper


def triangulate_layer(pb, layer, order=1):
    try:
        z = layer[0].z

        points = [(p.x, p.y) for p in layer]

        tris = polytri.triangulate(points)

        for triangle in tris:
            pb.triangle(*[Vec3(p[0], p[1], z) for p in triangle][::order])
    except ValueError as e:
        print(e)


class IndexedPoint:
    def __init__(self, point, index):
        self.point = point
        self.index = index


def rings_to_polyhedron(rings, progress_stdout=False):
    """
    Given a stack of polygons, turn it into a polyhedron

    This function doesn't work quite right ....

    Arguments:
        rings: list of list of Vec3 - Each list of Vec3s is a layer in a stack
    """

    pb = PolyhedronBuilder()

    it = enumerate(rings)
    if progress_stdout:
        it = tqdm(it, total=len(rings))
    for i, ring0 in it:
        if i == len(rings) - 1:
            break

        ring1 = rings[i + 1]

        # Reorder ring1
        # Start by finding the point on ring1 closest to ring0[0]. That will be ring1_ordered[0]
        # ring0_index = 0
        # Then, while there are remaining points on ring1, find the next point that has the smallest (distance to the previous ring1 point + min(distance to ring0[ring0_index], distance to ring0[ring0_index+1]))
        # If distance to ring0[ring0_index+1] was smaller, ring0_index += 1
        """
        ring1_to_add = ring1[:] # Copy list
        iring1 = []
        # Find point on ring1 closest to ring0[0]
        closest_index, closest_point = min(enumerate(ring1_to_add), key=lambda ip: ip[1].distance2(ring0[0]))
        iring1.append(IndexedPoint(closest_point, 0))
        del ring1_to_add[closest_index]

        ring0_index = 0
        while len(ring1_to_add) > 0:
            closest_to_current_index, closest_to_current_point, closest_to_current_distance = min([
                (i, p, p.distance(iring1[-1].point) + p.distance(ring0[ring0_index])) for i, p in enumerate(ring1_to_add)
            ], key=lambda ipd: ipd[2])

            closest_to_next_index, closest_to_next_point, closest_to_next_distance = min([
                (i, p, p.distance(iring1[-1].point) + p.distance(ring0[(ring0_index+1)%len(ring0)])) for i, p in enumerate(ring1_to_add)
            ], key=lambda ipd: ipd[2])

            if closest_to_current_distance < closest_to_next_distance:
                iring1.append(IndexedPoint(closest_to_current_point, ring0_index))
                del ring1_to_add[closest_to_current_index]
            else:
                ring0_index = (ring0_index + 1) % len(ring0)
                iring1.append(IndexedPoint(closest_to_next_point, ring0_index))
                del ring1_to_add[closest_to_next_index]
        """

        iring1 = []
        for p1 in ring1:
            min_index, min_point = min(
                enumerate(ring0),
                key=lambda p: Vec3(p[1].x, p[1].y).distance2(Vec3(p1.x, p1.y)),
            )
            iring1.append(IndexedPoint(p1, min_index))

        initial_iring1 = iring1[:]
        while True:
            # Rotate list
            iring1 = deque(iring1)
            min_value = min(iring1, key=lambda i: i.index)
            # TODO: we can probably do this in one rotate
            while (
                iring1[0].index != min_value.index
                or iring1[-1].index == min_value.index
            ):
                iring1.rotate(1)

            iring1 = list(iring1)

            # Assert that iring1 indicies are ordered
            last_index = iring1[0].index
            for i, ip in enumerate(iring1):
                if ip.index < last_index:
                    # Out of order index, see if previous or next point is closer
                    prev_dist = ip.point.distance2(ring0[last_index % len(ring0)])
                    next_dist = ip.point.distance2(ring0[(last_index + 1) % len(ring0)])
                    ip.index = last_index
                    if next_dist < prev_dist:
                        ip.index += 1
                last_index = ip.index

            # If the iring indicies rotate back around to zero, things get complicated, so lets take those values and add the length of ring0 to them
            for i in range(1, len(iring1)):
                if iring1[i].index < iring1[i - 1].index:
                    iring1[i].index += len(ring0)

            if iring1 == initial_iring1:
                break
            else:
                initial_iring1 = iring1[:]

        i0 = 0
        i1 = 0
        side = False
        while True:
            r0_a = ring0[i0 % len(ring0)]
            r0_b = ring0[(i0 + 1) % len(ring0)]
            r1i_a = iring1[i1 % len(iring1)]
            r1i_b = iring1[(i1 + 1) % len(ring1)]

            r1_a = r1i_a.point
            r1_b = r1i_b.point

            if side:
                pb.triangle(r0_a, r1_a, r1_b)

                i1 += 1

                if i0 >= len(ring0) and i1 >= len(ring1):
                    break

                if r1i_b.index > i0 or i1 >= len(ring1):
                    side = False
            else:
                pb.triangle(r0_a, r1_a, r0_b)

                i0 += 1

                if i0 >= len(ring0) and i1 >= len(ring1):
                    break

                if i0 > r1i_a.index or i0 >= len(ring0):
                    side = True

    triangulate_layer(pb, rings[0])
    triangulate_layer(pb, rings[-1], order=-1)

    return pb.build()


def similar_rings_to_polyhedron(rings, progress_stdout=True):
    pb = PolyhedronBuilder()

    it = enumerate(rings)
    if progress_stdout:
        it = tqdm(it, total=len(rings))
    for ri, ring0 in it:
        if ri == len(rings) - 1:
            break

        ring1 = rings[ri + 1]

        # Rotate ring 1
        ring1 = deque(ring1)
        closest_index, closest_point = min(
            enumerate(ring1), key=lambda ip: ip[1].distance2(ring0[0])
        )
        ring1.rotate(-closest_index)

        ring1 = list(ring1)

        rings[ri + 1] = ring1

        if len(ring1) != len(ring0):
            raise Exception("Rings not same length")

        for i in range(0, len(ring0)):
            r0a = ring0[i]
            r0b = ring0[(i + 1) % len(ring0)]
            r1a = ring1[i]
            r1b = ring1[(i + 1) % len(ring1)]

            pb.triangle(r0a, r1a, r0b)
            pb.triangle(r1a, r1b, r0b)

    triangulate_layer(pb, rings[0])
    triangulate_layer(pb, rings[-1], order=-1)

    return pb.build()


class PolyhedronBuilder:
    def __init__(self, build_graph=False):
        self.point_index = {}
        self.points = []
        self.triangles = []

        self.build_graph = build_graph
        if build_graph:
            self.adjacent = defaultdict(set)

    def add_point(self, v):
        p = (v.x, v.y, v.z)
        if p not in self.point_index:
            self.point_index[p] = len(self.points)
            self.points.append(p)
        return self.point_index[p]

    def triangle(self, v0, v1, v2):
        i0 = self.add_point(v0)
        i1 = self.add_point(v1)
        i2 = self.add_point(v2)

        if self.build_graph:
            self.adjacent[i0].add(i1)
            self.adjacent[i0].add(i2)

            self.adjacent[i1].add(i0)
            self.adjacent[i1].add(i2)

            self.adjacent[i2].add(i1)
            self.adjacent[i2].add(i0)

        self.triangles.append((i0, i1, i2))

    def build(self):
        return polyhedron(points=self.points, faces=self.triangles)


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...

    https://stackoverflow.com/questions/5434891/iterate-a-list-as-pair-current-next-in-python
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
