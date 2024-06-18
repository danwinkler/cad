class Poly:
    """A polygon defined by a list of points. The polygon must lie on an axis-aligned plane. The points must be integers."""

    def __init__(self, points: list[tuple[int, int, int]]):
        self.points = points

    def get_plane_normal(self) -> tuple[int, int, int]:
        """Return the normal vector of the plane in which the polygon lies."""
        p0, p1, p2 = self.points[:3]
        v1 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        v2 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    def intersects(self, other):
        other_normal = other.get_plane_normal()
        other_point = other.points[0]

        for p0, p1 in zip(self.points, self.points[1:] + [self.points[0]]):
            print(p0, p1)


if __name__ == "__main__":
    poly0 = Poly([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    poly1 = Poly([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)])

    poly0.intersects(poly1)
