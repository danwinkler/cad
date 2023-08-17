import math

from solid import *
from solid.utils import *

from cad.common import pyconvsurf
from cad.common.helper import *

parts = []

length = 80
height = 30
lip = 8


def basic_shape():
    surf = pyconvsurf.ConvSurf(margin=15, resolution=1)
    s = 1.1
    surf.add_line([0, 0, 0], [0, height, 0], s=s)
    surf.add_line([0, 0, 0], [length, height, 0], s=s)
    surf.add_line([length, height, 0], [0, height, 0], s=s)
    surf.add_line([length, height, 0], [length, height + lip, 0], s=s)

    vertices, triangles = surf.generate()
    print(f"num vertices: {len(vertices)}")
    return polyhedron(points=vertices, faces=triangles)


side_cut = 5
bottom_remove = hole()(
    translate([-10, -10, -side_cut * 2])(
        cube([length + 20, height + lip + 20, side_cut])
    ),
    translate([-10, -10, side_cut])(cube([length + 20, height + lip + 20, side_cut])),
)

back_remove = hole()(translate([-10, -10, -10])(cube([10, height + 20, 20])))

hole_y_offset = -5
hole_angle = 45
first_hole_rad = 10
screw_head_top_rad = 4
screw_bottom_rad = 2
screw_cone_height = 3.5

# Screw sections
# A: small section for screw
# B: tapered section
# C: large section for head of screw
a_rad = 2
a_length = 4
b_length = 3.5
c_rad = 4
c_length = 20
segments = 24

hole_remove = hole()(
    translate([0, height + hole_y_offset, 0])(
        # Rotate horizontal cylinders to angle
        rotate(a=-hole_angle, v=[0, 0, 1])(
            # Rotate vertical cylinders onto their side
            rotate(a=-90, v=[1, 0, 0])(
                down(a_rad)(
                    cylinder(r=a_rad, h=a_rad + a_length + 0.01, segments=segments),
                ),
                up(a_length)(
                    cylinder(
                        r1=a_rad,
                        r2=c_rad,
                        h=b_length + 0.01,
                        segments=segments,
                    )
                ),
                up(a_length + b_length)(
                    cylinder(
                        r=c_rad,
                        h=c_length,
                        segments=segments,
                    )
                ),
            )
        )
    ),
)

parts += [basic_shape(), back_remove, bottom_remove, hole_remove]

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
