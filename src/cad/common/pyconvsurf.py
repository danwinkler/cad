import time
import math
import numba
import numpy as np
from numba import float32, float64, guvectorize, njit, vectorize, cuda
import mcubes


@cuda.jit(device=True, inline=True)
def length2(a):
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2]


@cuda.jit(device=True, inline=True)
def length(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


@cuda.jit(device=True, inline=True)
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@cuda.jit(device=True, inline=True)
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


@cuda.jit(device=True, inline=True)
def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


@cuda.jit(device=True, inline=True)
def scale(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)


@cuda.jit(device=True, inline=True)
def line(p, p0, p1, s):
    # p is r in paper notation
    # p0 is b in paper notation
    v = sub(p1, p0)
    # v is a in paper notation

    l = length(v)
    l2 = l * l

    vn = (v[0], v[1], v[2])  # Copy
    vn = scale(vn, 1.0 / l)

    s2 = s * s

    # d = r - b
    d = sub(p, p0)

    dl2 = length2(d)

    # d_length = math.sqrt(dl2)
    # dnorm = (d[0] / d_length, d[1] / d_length, d[2] / d_length)

    # d should not be normalized, a (vn) should be normalized.
    # paper: x = da
    x = dot(d, vn)
    x2 = x * x

    # paper: p^2 = 1 + s^2(d^2 - x^2)
    p2 = 1 + (s2 * (dl2 - x2))
    pl = math.sqrt(p2)
    # paper: q^2 = 1 + s^2(d^2 + l^2 - 2lx)
    q2 = 1 + (s2 * (dl2 + l2 - (2 * l * x)))

    t1 = x / (2 * p2 * (p2 + s2 * x2))
    t2 = (l - x) / (2 * p2 * q2)
    t3 = (1 / (2 * s * pl * pl * pl)) * (
        math.atan((s * x) / pl) + math.atan((s * (l - x)) / pl)
    )

    return t1 + t2 + t3


print("Start compile (cuda fn)")
start = time.time()


@guvectorize(
    [(float64[:], float64[:, :, :], float64[:])],
    "(i),(j, k, l)->()",
    nopython=True,
    target="cuda",
)
def cuda_calculate_field(point, triangles, res):
    field_sum = 0
    for triangle in triangles:
        p0 = triangle[0]
        p1 = triangle[1]
        p2 = triangle[2]
        s = triangle[3][0]

        # Ugly hack to encode line as triangle
        if math.isnan(p2[0]):
            line_v = line(point, p0, p1, s)
            if not math.isnan(line_v) and line_v < 10000000:
                field_sum += line_v
            continue

        p0p1 = length(sub(p0, p1))
        p1p2 = length(sub(p1, p2))
        p2p0 = length(sub(p2, p0))

        if p1p2 > p0p1 and p1p2 > p2p0:
            # If p1p2 is longest
            p0t = p1
            p1t = p2
            p2t = p0

            p0 = p0t
            p1 = p1t
            p2 = p2t
        elif p2p0 > p0p1 and p2p0 > p1p2:
            # If p2p0 is longest
            p0t = p2
            p1t = p0
            p2t = p1

            p0 = p0t
            p1 = p1t
            p2 = p2t

        v01 = sub(p1, p0)
        v01length = length(v01)
        v02 = sub(p2, p0)

        # Appears to be unused
        # v02length = length(v01)

        # Normalized vectors
        # TODO: these were being set in the java version but appear to be unused
        # v01n = v01 / v01length
        # v02n = v02 / v02length

        # TODO: comment explaining this
        av = scale(v01, (dot(v01, v02) / dot(v01, v01)))

        b = add(p0, av)

        u = scale(v01, 1.0 / v01length)

        v = sub(p2, b)
        h = length(v)
        v = scale(v, 1.0 / h)  # Normalize v

        a1 = length(av)
        a2 = v01length - a1

        h2 = h * h
        s2 = s * s

        d = sub(point, b)

        d2 = length2(d)

        us = dot(d, u)
        vs = dot(d, v)

        us2 = us * us

        g = vs - h
        q = 1 + s2 * (d2 - us2 - vs * vs)
        C2 = 1 + s2 * (d2 - us2)
        w = C2 - 2 * h * s2 * vs + h2 * s2
        m = a2 * g + us * h
        n = us * h - a1 * g
        A2 = a1 * a1 * w + h2 * (q + s2 * us2) - 2 * h * s2 * a1 * us * g
        B2 = a2 * a2 * w + h2 * (q + s2 * us2) + 2 * h * s2 * a2 * us * g

        A = math.sqrt(A2)
        B = math.sqrt(B2)
        C = math.sqrt(C2)

        numer0 = s * (vs * h + a1 * (a1 + us))
        numer1 = s * (g * h + a1 * us)
        numer2 = s * (vs * h + a2 * (a2 - us))
        numer3 = s * (g * h - a2 * us)
        numer4 = s * (a1 + us)
        numer5 = s * (a2 - us)

        T1 = (n / A) * (math.atan(numer0 / A) + math.atan(numer1 / -A))
        T2 = (m / B) * (math.atan(numer2 / -B) + math.atan(numer3 / B))
        T3 = (vs / C) * (math.atan(numer4 / C) + math.atan(numer5 / C))

        field_sum += (1.0 / (2.0 * q * s)) * (T1 + T2 + T3)

    res[0] = field_sum


end = time.time()

print(f"Finished compile (cuda fn), took {end-start:2f} seconds")


def round_down(num, divisor):
    return num - (num % divisor)


def round_up(x, divisor):
    return int(math.ceil(x / divisor)) * divisor


def generate_field(minx, miny, minz, maxx, maxy, maxz, resolution):
    x = np.arange(minx, maxx, resolution)
    y = np.arange(miny, maxy, resolution)
    z = np.arange(minz, maxz, resolution)

    meshgrid = np.meshgrid(x, y, z)
    return np.vstack(meshgrid).reshape(3, -1).T, x.shape[0], y.shape[0], z.shape[0]


class ConvSurf:
    def __init__(self, margin, resolution):
        self.triangles = []
        self.margin = margin
        self.resolution = float(resolution)
        self.minx = 0
        self.miny = 0
        self.minz = 0
        self.maxx = 0
        self.maxy = 0
        self.maxz = 0

    def add_line(self, p0, p1, s=2):
        p0 = [float(p0[0]), float(p0[1]), float(p0[2])]
        p1 = [float(p1[0]), float(p1[1]), float(p1[2])]
        s = float(s)
        self.minx = min(self.minx, p0[0], p1[0])
        self.miny = min(self.miny, p0[1], p1[1])
        self.minz = min(self.minz, p0[2], p1[2])
        self.maxx = max(self.maxx, p0[0], p1[0])
        self.maxy = max(self.maxy, p0[1], p1[1])
        self.maxz = max(self.maxz, p0[2], p1[2])
        self.triangles.append([p0, p1, [math.nan, math.nan, math.nan], [s, 0.0, 0.0]])

    def add_triangle(self, p0, p1, p2, s=2):
        p0 = [float(p0[0]), float(p0[1]), float(p0[2])]
        p1 = [float(p1[0]), float(p1[1]), float(p1[2])]
        p2 = [float(p2[0]), float(p2[1]), float(p2[2])]
        s = float(s)
        self.minx = min(self.minx, p0[0], p1[0], p2[0])
        self.miny = min(self.miny, p0[1], p1[1], p2[1])
        self.minz = min(self.minz, p0[2], p1[2], p2[2])
        self.maxx = max(self.maxx, p0[0], p1[0], p2[0])
        self.maxy = max(self.maxy, p0[1], p1[1], p2[1])
        self.maxz = max(self.maxz, p0[2], p1[2], p2[2])
        self.triangles.append([p0, p1, p2, [s, 0.0, 0.0]])

    def add_rect(self, p0, p1, p2, p3, s=2):
        self.add_triangle(p0, p1, p2, s)
        self.add_triangle(p0, p2, p3, s)

    def generate(self, flip_winding=False, isovalue=0.005):
        # TODO: this currently doesn't work, the field is not generated correctly unless min and max are set by user before calling generate
        # Maybe try something like
        self.minx = round_down(self.minx - self.margin, self.resolution)
        self.miny = round_down(self.miny - self.margin, self.resolution)
        self.minz = round_down(self.minz - self.margin, self.resolution)
        self.maxx = round_up(self.maxx + self.margin, self.resolution)
        self.maxy = round_up(self.maxy + self.margin, self.resolution)
        self.maxz = round_up(self.maxz + self.margin, self.resolution)

        field, width, height, depth = generate_field(
            self.minx,
            self.miny,
            self.minz,
            self.maxx,
            self.maxy,
            self.maxz,
            self.resolution,
        )

        np_triangles = np.array(self.triangles)

        assert np_triangles.dtype == np.float64
        assert field.dtype == np.float64

        field = cuda_calculate_field(field, np_triangles)

        # Marching cubes has a different assumption about the shape of the field,
        # and I don't totally understand the details here
        vertices, triangles = mcubes.marching_cubes(
            field.reshape(height, width, depth), isovalue
        )

        # Note the switched x and y from the output of marching cubes
        vertices = [
            [
                v[1] * self.resolution + self.minx,
                v[0] * self.resolution + self.miny,
                v[2] * self.resolution + self.minz,
            ]
            for v in vertices
        ]

        if flip_winding:
            triangles = [[t[2], t[1], t[0]] for t in triangles]

        return vertices, triangles
