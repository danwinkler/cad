from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..assembly import PartInstance


class Joint(Protocol):
    id: str

    def participants(self) -> tuple[PartInstance, PartInstance]: ...


@dataclass
class RigidJoint:
    id: str
    a: PartInstance
    b: PartInstance

    def participants(self):
        return self.a, self.b
