from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []


def gear(rad=30, thickness=4, hole_rad=4, num_teeth=13, b=4, teeth_width=6):
    teeth_half_width = teeth_width / 2
    base = difference()(
        cylinder(r=rad - b, h=thickness), down(1)(cylinder(r=hole_rad, h=thickness + 2))
    )
    p = (360.0) / num_teeth
    teeth = []
    for i in xrange(num_teeth):
        r = p * i
        teeth.append(
            rotate(r, [0, 0, 1])(
                translate([0, rad - b, 0])(
                    linear_extrude(height=thickness)(
                        polygon(
                            points=[
                                [-teeth_half_width, -10],
                                [-teeth_half_width, b],
                                [-(teeth_half_width - 2), b * 2],
                                [(teeth_half_width - 2), b * 2],
                                [teeth_half_width, b],
                                [(teeth_half_width), -10],
                            ]
                        )
                    )
                )
            )
        )

    return union()(teeth) + base


def base():
    return union()(
        cube([20, 80, 5]),
        translate([10, 10, 0])(cylinder(h=9, r=3.5)),
        translate([10, 70, 0])(cylinder(h=20, r=3.5)),
    )


def bar():
    return difference()(
        cube([16, 150, 4]),
        translate([8, 8, -1])(cylinder(r=4, h=6)),
        hull()(
            translate([8, 8 + (60 + 20), -1])(cylinder(r=4, h=6)),
            translate([8, 8 + (60 - 20), -1])(cylinder(r=4, h=6)),
        ),
    )


def box():
    return union()(
        cube([20, 5, (30 * 2) + (4 * 2)]),
        translate([10, 1, 68 - (30 - 4) - 1])(
            rotate(90, [1, 0, 0])(cylinder(r=3.5, h=20))
        ),
        translate([0, 0, 68 - 5])(cube([20, (30 - 4 + 1) * 2, 5])),
        translate([10, 30 + 1 - 4, 30 * 2 + 4 * 2 - 1])(cylinder(r=3.5, h=20)),
        translate([0, (30 - 4 + 1) * 2 - 5, 0])(cube([20, 5, (30 * 2) + (4 * 2)])),
        translate([10, (30 - 4 + 1) * 2 - 1, 68 - (30 - 4) - 1])(
            rotate(-90, [1, 0, 0])(cylinder(r=3.5, h=20))
        ),
    )


"""
parts.append( 
	translate( [10,10,6] ) ( rotate( -2, [0,0,1] ) ( gear() ) )
)

parts.append( 
	translate( [10,70,6] ) ( 
		rotate( 360/13.0 + 6, [0,0,1] ) (
			gear()
		)
	)
)
"""

# parts.append( gear() )
# parts.append( left( 20 ) ( cylinder( r=3.5, h=15 ) ) )

# parts.append( translate( [35, -75, 0] ) ( bar() ) )

# parts.append( base() )

# parts.append( gear() )

parts.append(box())
# parts.append( translate( [10,-1,68-(30-4)-1] ) ( rotate( 90, [1,0,0] ) ( gear() ) ) )
# parts.append( translate( [10,30+1-4,30*2+4*2+1] ) ( gear() ) )
# parts.append( translate( [10,(30-4+1)*2+1,68-(30-4)-1] ) ( rotate( -90, [1,0,0] ) ( gear() ) ) )

# parts.append( left( 40 ) ( gear() ) )

# parts.append( translate( [-40,65,0] ) ( gear() ) )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
