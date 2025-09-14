from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

from shapely.geometry import Polygon

from cad.common import gear as legacy_gear


@dataclass
class GearProfileResult:
    polygon: Polygon
    pitch_radius: float
    outer_radius: float
    addendum: float
    dedendum: float


def generate_gear_profile(
    teeth: int,
    tooth_width: float,
    pressure_angle_deg: float,
    backlash: float,
    frame_count: int,
) -> GearProfileResult:
    """Generate gear polygon and radii using legacy generator plus derived metrics.

    Returns GearProfileResult with pitch, outer, addendum, dedendum radii.
    """
    # Use effective tooth width reduced by backlash for radius calculations (mirror legacy logic)
    eff_tooth_width = tooth_width - backlash
    pitch_circumference = eff_tooth_width * 2 * teeth
    pitch_radius = pitch_circumference / (2 * math.pi)
    addendum = eff_tooth_width * (2 / math.pi)
    dedendum = addendum  # symmetrical in legacy algorithm
    outer_radius = pitch_radius + addendum

    poly, legacy_pitch_radius = legacy_gear.generate(
        teeth_count=teeth,
        tooth_width=tooth_width,
        pressure_angle=legacy_gear.deg2rad(pressure_angle_deg),
        backlash=backlash,
        frame_count=frame_count,
    )
    # legacy returns pitch_radius (should align closely with computed pitch_radius using eff width)
    # prefer the explicit computed one with effective width for consistency of outer radius calculation
    return GearProfileResult(
        polygon=poly,
        pitch_radius=pitch_radius,
        outer_radius=outer_radius,
        addendum=addendum,
        dedendum=dedendum,
    )
