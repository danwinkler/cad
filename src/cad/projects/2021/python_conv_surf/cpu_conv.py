import time
import math
import numba
import numpy as np
from numba import float32, float64, guvectorize, njit, vectorize, cuda


@njit(inline="always")
def length2(a):
    return a[0] ** 2 + a[1] ** 2 + a[2] ** 2


@njit(inline="always")
def length(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


@njit(inline="always")
def normalize(a):
    return a / length(a)


@njit(inline="always")
def dot(a, b):
    return (a * b).sum()


print("Start compile")
start = time.time()


@guvectorize(
    [(float64[:], float64[:, :, :], float64[:])],
    "(i),(j, k, l)->()",
    nopython=True,
    target="parallel",
    cache=True,
)
def calculate_field(point, triangles, res):
    field_sum = 0
    for triangle in triangles:
        p0 = triangle[0]
        p1 = triangle[1]
        p2 = triangle[2]
        s = triangle[3][0]
        p0p1 = length(p0 - p1)
        p1p2 = length(p1 - p2)
        p2p0 = length(p2 - p0)

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

        v01 = p1 - p0
        v01length = length(v01)
        v02 = p2 - p0

        # Appears to be unused
        # v02length = length(v01)

        # Normalized vectors
        # TODO: these were being set in the java version but appear to be unused
        # v01n = v01 / v01length
        # v02n = v02 / v02length

        # TODO: comment explaining this
        av = v01 * (dot(v01, v02) / dot(v01, v01))

        b = p0 + av

        u = v01 / v01length

        v = p2 - b
        h = length(v)
        v = v / h  # Normalize v

        a1 = length(av)
        a2 = v01length - a1

        h2 = h * h
        s2 = s * s

        d = point - b

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

print(f"Finished compile, took {end-start:2f} seconds")
