from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from .definitions.base import BuildContext, PartDefinition
from .geometry import Profile2D, Transform


@dataclass
class PartInstance:
    id: str
    definition: PartDefinition
    transform: Transform = field(default_factory=Transform.identity)
    material: dict | None = None
    tags: set[str] = field(default_factory=set)


class Assembly:
    def __init__(self, name: str | None = None):
        self.name = name
        self.parts: list[PartInstance] = []
        self.joints: list = []  # generic until joints implemented
        self._ctx = BuildContext(cache={})
        self._id_counter = 0

    def _next_id(self, prefix: str = "pi"):
        self._id_counter += 1
        return f"{prefix}{self._id_counter}"

    def add_part(
        self,
        definition: PartDefinition,
        transform: Transform | None = None,
        material: dict | None = None,
        tags: Iterable[str] | None = None,
    ) -> PartInstance:
        inst = PartInstance(
            id=self._next_id(),
            definition=definition,
            transform=transform or Transform.identity(),
            material=material,
            tags=set(tags) if tags else set(),
        )
        self.parts.append(inst)
        return inst

    def add_joint(self, joint):
        self.joints.append(joint)
        return joint

    def solve(self, solver=None):
        # placeholder; when solver added it will update transforms based on joints
        if solver:
            solver.solve(self)

    def iter_sheet_profiles(self) -> list[tuple[PartInstance, Profile2D]]:
        out = []
        for p in self.parts:
            if p.definition.kind() == "sheet":
                prof = p.definition.get_profile_2d(self._ctx)
                if prof:
                    out.append((p, prof))
        return out

    def export(self, exporter, selection: Optional[list[PartInstance]] = None, **opts):
        selection = selection or self.parts
        return exporter.emit(self, selection, **opts)

    def to_dict(self, include_geometry: bool = True):
        parts_out = []
        for p in self.parts:
            entry = {
                "id": p.id,
                "definition_id": getattr(p.definition, "id", None),
                "kind": p.definition.kind(),
                "transform": p.transform.to_json(),
                "parameters": p.definition.parameters(),
                "tags": sorted(list(p.tags)),
            }
            if p.material:
                entry["material"] = p.material
            if include_geometry and p.definition.kind() == "sheet":
                prof = p.definition.get_profile_2d(self._ctx)
                if prof:
                    geom = prof.geometry
                    # serialize as list of polygons: each = {exterior: [[x,y],...], holes: [...]}
                    polys = []
                    if geom.geom_type == "Polygon":
                        geom_list = [geom]
                    else:
                        geom_list = list(geom.geoms)
                    for poly in geom_list:
                        polys.append(
                            {
                                "exterior": list(map(list, poly.exterior.coords)),
                                "holes": [
                                    list(map(list, i.coords)) for i in poly.interiors
                                ],
                            }
                        )
                    entry["profile2d"] = {"polygons": polys, "metadata": prof.metadata}
            parts_out.append(entry)

        joints_out = []
        for j in self.joints:
            # basic gear joint serialization
            j_type = j.__class__.__name__
            data = {"id": getattr(j, "id", None), "type": j_type}
            if j_type == "GearJoint":
                data.update(
                    {
                        "driver": j.driver.id,
                        "driven": j.driven.id,
                        "ratio": j.ratio,
                        "backlash": j.backlash,
                    }
                )
            joints_out.append(data)

        return {
            "name": self.name,
            "parts": parts_out,
            "joints": joints_out,
            "version": 1,
        }
