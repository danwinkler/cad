import time
import math
import numba
import numpy as np
from numba import float32, float64, guvectorize, njit, vectorize, cuda


@cuda.jit(device=True, inline=True)
def length2(a):
    return a[0] ** 2 + a[1] ** 2 + a[2] ** 2


@cuda.jit(device=True, inline=True)
def length(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


@cuda.jit(device=True, inline=True)
def normalize(a):
    return a / length(a)


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
    v = sub(p1, p0)

    l = length(v)
    l2 = l * l

    vn = (v[0], v[1], v[2])  # Copy
    vn = scale(vn, 1.0 / l)

    s2 = s * s

    d = sub(p, p0)

    dl2 = length2(d)

    x = dot(d, vn)
    x2 = x * x
    p2 = 1 + s2 * (dl2 - x2)
    pl = math.sqrt(p2)
    q2 = 1 + s2 * (dl2 + l2 - 2 * l * x)

    t1 = x / (2 * p2 * (p2 + s2 * x2))
    t2 = (l - x) / (2 * p2 * q2)
    t3 = (1 / (2 * s * p2 * pl)) * (
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
            field_sum += line(point, p0, p1, s)
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
