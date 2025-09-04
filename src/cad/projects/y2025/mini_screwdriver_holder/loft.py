import math
from typing import Any, List, Optional, Sequence, Tuple

from shapely import affinity as _aff
from shapely.geometry import LineString
from shapely.geometry import Polygon as _Polygon
from shapely.geometry.polygon import orient as _orient

Vec2 = Tuple[float, float]
Vec3 = Tuple[float, float, float]
Tri = Tuple[int, int, int]

# ---------------- Helpers: input + resampling via Shapely ----------------


def _to_polygon(obj: Any, name: str) -> _Polygon:
    """
    Accept a Shapely Polygon or a sequence of (x,y) and return a Shapely Polygon.
    Rejects holes.
    """
    if isinstance(obj, _Polygon):
        poly = obj
    elif isinstance(obj, Sequence) and len(obj) >= 3:
        poly = _Polygon([(float(x), float(y)) for x, y in obj])  # may auto-close
    else:
        raise TypeError(f"{name} must be a shapely Polygon or a sequence of (x,y)")

    if not poly.is_valid:
        # If you truly have simple polygons, this shouldn't trigger.
        # For safety you could do: poly = poly.buffer(0) to 'nudge' validity.
        raise ValueError(
            f"{name} polygon is invalid: {poly.explain_validity() if hasattr(poly,'explain_validity') else ''}"
        )

    if len(poly.interiors) > 0:
        raise ValueError(
            f"{name} polygon has holes; only hole-free polygons are supported."
        )

    # Ensure CCW orientation (positive area in XY)
    return _orient(poly, sign=1.0)


def _resample_exterior(poly: _Polygon, n: int) -> List[Vec2]:
    """
    Evenly sample n points along the polygon perimeter (excluding the duplicate end).
    Uses Shapely's linear referencing on the exterior boundary.
    """
    if n < 3:
        raise ValueError("n must be >= 3")
    ring = LineString(list(poly.exterior.coords))  # includes closing point
    pts: List[Vec2] = []
    for i in range(n):
        # normalized=True -> distance is fraction of total length in [0,1]
        p = ring.interpolate(i / n, normalized=True)
        pts.append((p.x, p.y))
    return pts


# ---------------- Ear-clipping triangulation (keep: it’s constrained) ----------------


def _is_point_in_triangle(p: Vec2, a: Vec2, b: Vec2, c: Vec2) -> bool:
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(p, a, b) < 0.0
    b2 = sign(p, b, c) < 0.0
    b3 = sign(p, c, a) < 0.0
    return (b1 == b2) and (b2 == b3)


def _is_convex(a: Vec2, b: Vec2, c: Vec2) -> bool:
    return ((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 0


def _triangulate_ccw(poly: List[Vec2]) -> List[Tri]:
    n = len(poly)
    if n < 3:
        return []
    V = list(range(n))
    tris: List[Tri] = []
    guard = 0
    while len(V) > 3 and guard < 10000:
        guard += 1
        ear_found = False
        for i in range(len(V)):
            i_prev = V[(i - 1) % len(V)]
            i_curr = V[i]
            i_next = V[(i + 1) % len(V)]
            a, b, c = poly[i_prev], poly[i_curr], poly[i_next]
            if not _is_convex(a, b, c):
                continue
            ear = True
            for j in V:
                if j in (i_prev, i_curr, i_next):
                    continue
                if _is_point_in_triangle(poly[j], a, b, c):
                    ear = False
                    break
            if ear:
                tris.append((i_prev, i_curr, i_next))
                del V[i]
                ear_found = True
                break
        if not ear_found:
            # Degenerate / nearly self-intersecting case
            break
    if len(V) == 3:
        tris.append((V[0], V[1], V[2]))
    return tris


# ---------------- Main loft (Shapely-powered orientation/transform/sampling) ----------------


def _lcm(a: int, b: int) -> int:
    import math as _m

    return a * b // _m.gcd(a, b)


def loft_polygons(
    bottom: Any,
    top: Any,
    *,
    z0: float = 0.0,
    z1: float = 1.0,
    top_scale: Tuple[float, float] = (1.0, 1.0),
    top_rotation_rad: float = 0.0,
    top_translate: Tuple[float, float] = (0.0, 0.0),
    n_samples: Optional[int] = None,
    top_transform_origin: Tuple[float, float] = (
        0.0,
        0.0,
    ),  # change to (cx,cy) if you want to rotate/scale about centroid
) -> Tuple[List[Vec3], List[Tri]]:
    """
    Loft between two simple polygons (hole-free). 'bottom' and 'top' can be Shapely Polygons
    or sequences of (x,y). Uses Shapely to orient, transform, and resample evenly by arclength.
    """
    # Normalize to Shapely Polygons (CCW, hole-free)
    bottom_poly = _to_polygon(bottom, "bottom")
    top_poly = _to_polygon(top, "top")

    # Apply top transforms via Shapely affinity
    sx, sy = top_scale
    ox, oy = top_transform_origin
    top_poly = _aff.scale(top_poly, xfact=sx, yfact=sy, origin=(ox, oy))
    top_poly = _aff.rotate(
        top_poly, angle=top_rotation_rad, use_radians=True, origin=(ox, oy)
    )
    tx, ty = top_translate
    top_poly = _aff.translate(top_poly, xoff=tx, yoff=ty)

    # Choose sampling count (lcm of vertex counts, capped), then resample both by arclength
    nb = len(bottom_poly.exterior.coords) - 1  # minus duplicate close
    nt = len(top_poly.exterior.coords) - 1
    if n_samples is None:
        n_samples = _lcm(max(3, nb), max(3, nt))
        n_samples = max(max(nb, nt), min(n_samples, 2000))

    rb = _resample_exterior(bottom_poly, n_samples)  # CCW ring samples
    rt = _resample_exterior(top_poly, n_samples)

    # Vertices: bottom ring then top ring
    vertices: List[Vec3] = [(x, y, z0) for (x, y) in rb] + [(x, y, z1) for (x, y) in rt]

    # Side faces (quads split into two triangles)
    faces: List[Tri] = []
    N = n_samples
    for i in range(N):
        i0 = i
        i1 = (i + 1) % N
        j0 = N + i
        j1 = N + ((i + 1) % N)
        faces.append((i0, i1, j1))
        faces.append((i0, j1, j0))

    # Caps via ear-clipping on the sampled rings
    bottom_tris = _triangulate_ccw(rb)  # [0 .. N-1]
    top_tris = _triangulate_ccw(rt)  # reverse order for outward normal
    faces.extend(bottom_tris)
    faces.extend((N + c, N + b, N + a) for (a, b, c) in top_tris)

    return vertices, faces
