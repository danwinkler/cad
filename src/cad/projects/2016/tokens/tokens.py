import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *


def make_token():
    token = cylinder(r=10, h=5.5, segments=36)
    token -= down(1)(cylinder(r=8.5, h=3.5, segments=36))
    token -= up(4)(cylinder(r=10.5, h=3, segments=36) - cylinder(r=8, h=3, segments=36))
    return token


def plus_one():
    return linear_extrude(height=3)(
        text("+1", size=8, valign="center", halign="center")
    )


def plus_five():
    return linear_extrude(height=3)(
        text("+5", size=8, valign="center", halign="center")
    )


def neg_one():
    return linear_extrude(height=3)(
        text("-1", size=8, valign="center", halign="center")
    )


def poison():
    return linear_extrude(height=3)(
        text("\uE618", size=8, font="mana", valign="center", halign="center")
    )


def white():
    return linear_extrude(height=3)(
        text("\uE600", size=8, font="mana", valign="center", halign="center")
    )


def blue():
    return linear_extrude(height=3)(
        text("\uE601", size=8, font="mana", valign="center", halign="center")
    )


def black():
    return linear_extrude(height=3)(
        text("\uE602", size=8, font="mana", valign="center", halign="center")
    )


def red():
    return linear_extrude(height=3)(
        text("\uE603", size=8, font="mana", valign="center", halign="center")
    )


def green():
    return linear_extrude(height=3)(
        text("\uE604", size=8, font="mana", valign="center", halign="center")
    )


funs = [plus_one, plus_five, neg_one, poison, white, blue, black, red, green]

for f in funs:
    token = make_token()
    token -= translate([0, 0, 4.5])(f())

    print("Saving " + f.__name__)
    with open(f.__name__ + ".scad", "w") as f:
        f.write(scad_render(token))

import os
import subprocess

pgm = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
# pgm = "C:\Program Files (x86)\OpenSCAD\openscad.exe"


def get_structure_images():
    files = os.listdir(".")
    for file in files:
        if file[-5:] == ".scad":
            subprocess.call([pgm, "-o", file.replace(".scad", "") + ".stl", file])


get_structure_images()
