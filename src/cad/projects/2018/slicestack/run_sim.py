import pyclipper

from dan.lib import glfw
from dan.lib.helper import Vec3
from dan.project.slicestack.differential_line import DiffLine

from p5 import *


dl = DiffLine()

def setup():
    size(800, 600)
    # no_stroke()
    stroke(0)
    dl.init_circle()



def draw():
    dl.update()
    dl.update()

    background(255)
    

    push_matrix()
    translate(width * 0.5, height * 0.5)

    for nodes in dl.rings:
        for i, n in enumerate(nodes):
            line((n.pos.x, n.pos.y), (n.next.pos.x, n.next.pos.y))
    
    # for i, p in enumerate(shrunk_points):
    #     next = shrunk_points[(i + 1) % len(shrunk_points)]
    #     line((p.x, p.y), (next.x, next.y))

    reset_matrix()



run()
