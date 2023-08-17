from solid import *
from solid.utils import *

from cad.common.helper import *

base = up(5)(cube([24, 24, 10], center=True))
base -= cylinder(h=4.2, r=7.5)
base -= up(4.2 + (4.5 / 2.0))(cube([6.8, 6.8, 4.5], center=True))
base -= cylinder(h=12, r=6.8 / 2.0)

base = rotate(v=[0, 1, 0], a=180)(base)
base = up(10)(base)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(base))
