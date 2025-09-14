from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from shapely.geometry import MultiPolygon, Polygon

from ..geometry import Profile2D
from .base import BuildContext, PartDefinition


def _hash_polygon(poly: Polygon | MultiPolygon) -> str:
    if isinstance(poly, Polygon):
        polys = [poly]
    else:
        polys = list(poly.geoms)
    h = hashlib.sha1()
    for p in polys:
        h.update(str(list(p.exterior.coords)).encode())
        for interior in p.interiors:
            h.update(str(list(interior.coords)).encode())
    return h.hexdigest()[:10]


@dataclass
class SheetPartDefinition(PartDefinition):
    geometry: Polygon | MultiPolygon
    thickness: float
    id: str = field(default_factory=lambda: "sheet_")

    def __post_init__(self):
        object.__setattr__(self, "id", f"sheet_{_hash_polygon(self.geometry)}")

    def kind(self) -> str:
        return "sheet"

    def parameters(self) -> dict:
        return {"thickness": self.thickness}

    def get_profile_2d(self, ctx: BuildContext):
        return Profile2D(self.geometry, metadata={"thickness": self.thickness})
