from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union


@dataclass
class Profile2D:
    geometry: Polygon | MultiPolygon
    metadata: dict | None = None

    def union(self, other: "Profile2D") -> "Profile2D":
        return Profile2D(unary_union([self.geometry, other.geometry]))

    @property
    def bounds(self):
        return self.geometry.bounds
