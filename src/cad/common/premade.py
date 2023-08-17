from solid import *
from solid.utils import *
from collections import namedtuple

SPreset = namedtuple("SPreset", ["r", "r2", "csheight"])

screwhole_presets = {"#8 wood": SPreset(r=1.9, r2=4, csheight=3)}


def screwhole(preset_name, length, segments=12):
    p = screwhole_presets[preset_name.lower()]

    return hole()(
        down(length)(cylinder(r=p.r, h=length, segments=segments))
        + down(p.csheight)(cylinder(r1=p.r, r2=p.r2, h=p.csheight, segments=segments))
        + cylinder(r=p.r2, h=1, segments=segments)
    )
