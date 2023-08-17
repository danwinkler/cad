from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

f_size = 14
m_size = 14

m_length = 30
f_length = 30

outer_m = m_size + 1.5 + 0.5
outer_f = 0

middle_width = max(outer_m, outer_f)

parts.append(
    rotate(-90, [1, 0, 0])(
        union()(
            # Female side
            translate([0, 0, f_size / 2])(
                rotate(90, [0, 1, 0])(
                    translate([0, 0, -5])(
                        difference()(
                            union()(
                                translate([f_size / 2.0 - 3, -f_length + 10, 0])(
                                    cube([3, f_length, 10]),
                                ),
                                translate([-f_size / 2.0, -f_length + 10, 0])(
                                    cube([3, f_length, 10]),
                                ),
                            ),
                            translate([0, -f_length + 5 + 10, 5])(
                                rotate(90, [0, 1, 0])(
                                    cylinder(h=f_size + 2, r=3, center=True)
                                )
                            ),
                        )
                    )
                )
            ),
            # Middle
            translate([-middle_width / 2, 0, 0])(cube([middle_width, 10, 3])),
            translate([-middle_width / 2, 0, f_size - 3])(cube([middle_width, 10, 3])),
            # Male side
            translate([m_size / 2.0 + 0.5, 0, 0])(
                cube([3, m_length, f_size]),
                translate([0, m_length - 5, f_size / 2])(
                    rotate(90, [0, 1, 0])(cylinder(h=3, r=2.5, center=True))
                ),
            ),
            translate([-m_size / 2.0 - 3 - 0.5, 0, 0])(
                cube([3, m_length, f_size]),
                translate([3, m_length - 5, f_size / 2])(
                    rotate(90, [0, 1, 0])(cylinder(h=3, r=2.5, center=True))
                ),
            ),
        )
    )
)

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
