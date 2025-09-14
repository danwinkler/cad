from __future__ import annotations

from dataclasses import dataclass

from ..assembly import PartInstance


@dataclass
class GearJoint:
    id: str
    driver: PartInstance
    driven: PartInstance
    ratio: float | None = None  # teeth_driven / teeth_driver (computed if None)
    backlash: float = 0.0

    def participants(self):
        return self.driver, self.driven
