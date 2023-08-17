import math
import random

import visual as vi

from cad.common.helper import *

from .pointcloud import *

objs = [
    Line(Vec3(0, 0, 0), Vec3(0, 0, 1)),
    Line(Vec3(0, 0, 0), Vec3(1, 0, 0)),
    Line(Vec3(0, 0, 0), Vec3(0, 1, 0)),
]

# make_points_file( objs, "lines.xyz", min_bound=Vec3(-1, -1, -1 ), max_bound=Vec3( 1.5, 1.5, 1.5 ), resolution=.03 )
# make_points_file( objs, "lines.xyz", min_bound=Vec3(-1, -1, -1 ), max_bound=Vec3( 1.5, 1.5, 1.5 ), resolution=.03, field_function=BLOBBY, d=2, r=.1, function_opts=[2, 5] )
# make_points_file( objs, "lines.xyz", min_bound=Vec3(-3, -3, -3 ), max_bound=Vec3( 3, 3, 3 ), resolution=.03, field_function=METABALL, d=1, r=.1, function_opts=[1, 1] )
make_points_file(
    objs,
    "lines.xyz",
    min_bound=Vec3(-3, -3, -3),
    max_bound=Vec3(3, 3, 3),
    resolution=0.03,
    field_function=SOFT_OBJECT,
    d=1,
    r=0.1,
    function_opts=[1, 1],
)
