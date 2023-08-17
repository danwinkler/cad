from solid import *
from solid.utils import *


def mini_pushbutton(render_non_printable=True, substrate_thickness=10):
    subs = []
    parts = []
    if render_non_printable:
        pushbutton_xoffset = 3
        pushbutton_yoffset = 4
        pb = import_stl("mini_pushbutton.stl")
        parts += [translate([-pushbutton_xoffset, -pushbutton_yoffset])(pb)]

    subs += [cylinder(r=8, h=20)]
    subs += [translate([-10, -10, 0])(cube([20, 20, substrate_thickness - 5]))]

    return subs, parts


parts = []
subs = []

substrate = cube([100, 100, 10])

s, p = mini_pushbutton(substrate_thickness=10)
parts += translate([40, 40])(p)
subs += translate([40, 40])(s)

final_parts = [substrate - subs] + parts

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(final_parts)))
