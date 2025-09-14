from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from shapely.geometry import Polygon

from cad.common import (
    gear as legacy_gear,
)  # legacy retained for backward compat (deprecated direct use)

from ..gear import generate_gear_profile
from ..geometry import Profile2D
from .base import BuildContext, PartDefinition


def _gear_hash(
    teeth: int, tooth_width: float, pressure_angle: float, backlash: float
) -> str:
    h = hashlib.sha1(
        f"{teeth}-{tooth_width}-{pressure_angle}-{backlash}".encode()
    ).hexdigest()
    return h[:10]


@dataclass
class GearPartDefinition(PartDefinition):
    teeth: int
    tooth_width: float
    pressure_angle_deg: float = 20.0
    backlash: float = 0.0
    frame_count: int = 16
    thickness: float = 5.0
    id: str = field(init=False)

    def __post_init__(self):
        self.id = f"gear_{_gear_hash(self.teeth, self.tooth_width, self.pressure_angle_deg, self.backlash)}"

    def kind(self) -> str:
        return "sheet"  # currently 2D profile + thickness

    def parameters(self) -> dict:
        return {
            "teeth": self.teeth,
            "tooth_width": self.tooth_width,
            "pressure_angle_deg": self.pressure_angle_deg,
            "backlash": self.backlash,
            "thickness": self.thickness,
        }

    def get_profile_2d(self, ctx: BuildContext):
        res = generate_gear_profile(
            teeth=self.teeth,
            tooth_width=self.tooth_width,
            pressure_angle_deg=self.pressure_angle_deg,
            backlash=self.backlash,
            frame_count=self.frame_count,
        )
        return Profile2D(
            res.polygon,
            metadata={
                "pitch_radius": res.pitch_radius,
                "outer_radius": res.outer_radius,
                "addendum": res.addendum,
                "dedendum": res.dedendum,
                "thickness": self.thickness,
            },
        )
