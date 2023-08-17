import math
import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *


def gear_rad(count, teeth_width=4):
    c = teeth_width * count
    r = (c / math.pi) * 0.5
    return r


def gear(count, thickness, hole_rad, teeth_width=4):
    c = teeth_width * count
    r = (c / math.pi) * 0.5
    teeth_depth = teeth_width * 0.7

    teeth_holes = []
    for i in range(count):
        a = (360.0 / count) * i

        teeth_holes.append(
            down(0.5)(
                rotate(a, [0, 0, 1])(
                    translate([0, r + teeth_depth * 0.4, 0])(
                        linear_extrude(height=thickness + 1)(
                            polygon(
                                points=[
                                    [-teeth_width / 2.0, 0],
                                    [0, 1],
                                    [teeth_width / 2.0, 0],
                                    [0, -teeth_depth],
                                ]
                            )
                        )
                    )
                )
            )
        )

    return difference()(
        cylinder(r=r + (teeth_depth * 0.4), h=thickness),
        teeth_holes,
        down(1)(cylinder(h=thickness + 2, r=hole_rad)),
    )


parts = []

doublegear = gear(17, 9, 4) + gear(41, 4, 4)
parts.append(doublegear)

"""
parts.append( 
	translate( [gear_rad( 17 ) + gear_rad( 41 ), 0, 4.5] ) ( 
		doublegear +
		down( 4.5 ) ( cylinder( h=14, r=3.5 ) )
	) 
)
"""

# parts.append( up( 9.5 ) ( rotate( 360/41/2, [0,0,1] ) ( gear( 41, 4, 4 ) ) ) )

"""
parts.append( cylinder( h=14, r=3.5 ) )
parts.append( translate( [-10, -10, 0] ) ( 
	cube( [10 + gear_rad( 41 )*2 + gear_rad( 17 ) + 10, 20, 4] ) +
	cube( [10+3.5, 20, 4.5+4] )
))
"""

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
