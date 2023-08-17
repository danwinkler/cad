import math
import random
from collections import namedtuple

from numba import jit

from cad.common.helper import Vec3

_node_id = 0

# TODO: nested rings?


class NodeData:
    def __init__(self, node):
        self.pos = Vec3(node.pos)
        self.id = node.id
        self.prev = node.prev.id
        self.next = node.next.id

        # This is a helper field for trianglulation
        self.opposite = None


@jit(nopython=True)
def numba_push(ax, ay, bx, by, max_dist, scalar):
    dx = ax - bx
    dy = ay - by

    d2 = (dx * dx) + (dy * dy)

    if d2 > max_dist**2:
        return (0, 0)

    d = math.sqrt(d2)
    dxn = dx / d
    dyn = dy / d

    mag = (1 / (d * d)) * scalar
    return (dxn * mag, dyn * mag)


class Node:
    NEIGHBOR_DISTANCE = 3
    NEIGHBOR_PUSH_SCALAR = 0.05
    OTHER_PUSH_SCALAR = 8
    OTHER_RING_PUSH_SCALAR = 3
    MAX_DIST_OTHER = NEIGHBOR_DISTANCE * 5

    def __init__(self, x, y, ring_index):
        global _node_id
        self.pos = Vec3(x, y)
        self.pos_next = Vec3(self.pos)
        self.prev = None
        self.next = None
        self.ring_index = ring_index

        self.id = _node_id
        _node_id += 1

    def set_prev(self, node):
        if self.prev != node:
            self.prev = node
            node.set_next(self)

    def set_next(self, node):
        if self.next != node:
            self.next = node
            node.set_prev(self)

    def update(self, rings):
        # Maintain distance from neighbors
        self.pos_next.set(self.pos)

        self.neighbor_push(self.prev)
        self.neighbor_push(self.next)

        for ring_index, nodes in enumerate(rings):
            if self.ring_index == ring_index:
                scalar = Node.OTHER_PUSH_SCALAR
            else:
                scalar = Node.OTHER_RING_PUSH_SCALAR
            for node in nodes:
                if node in (self.next, self.prev, self):
                    continue

                self.other_push(node, scalar)

    def other_push(self, node, scalar):
        dx, dy = numba_push(
            self.pos.x, self.pos.y, node.pos.x, node.pos.y, self.MAX_DIST_OTHER, scalar
        )
        self.pos_next.x += dx
        self.pos_next.y += dy

        # vec = self.pos - node.pos
        # distance2 = vec.length2()

        # if distance2 > self.MAX_DIST_OTHER ** 2:
        #     return

        # distance = math.sqrt(distance2)
        # vec_norm = Vec3(vec)
        # vec_norm /= distance

        # push_force = vec_norm * ((1 / (distance*distance)) * scalar)

        # self.pos_next += push_force

    def neighbor_push(self, node):
        vec = self.pos - node.pos
        distance = vec.length()
        vec_norm = Vec3(vec)
        vec_norm /= distance

        distance_from_optimal = distance - self.NEIGHBOR_DISTANCE
        push_force = vec_norm * (distance_from_optimal * self.NEIGHBOR_PUSH_SCALAR)
        push_force *= -1

        self.pos_next += push_force

    def __repr__(self):
        return "<Node id:{} prev:{} next:{}>".format(
            self.id, self.prev.id, self.next.id
        )


RingDefinition = namedtuple("RingDefinition", ["radius", "growth_rate"])


class DiffLine:
    def __init__(self):
        self.roots = []
        self.rings = []
        random.seed(0)

    def init_circle(self):
        self.ring_defs = [
            RingDefinition(4, 0.9),
            RingDefinition(8, 0.5),
        ]

        for ring_index, ring_def in enumerate(self.ring_defs):
            num_points = math.floor(
                (ring_def.radius * math.pi * 2) / Node.NEIGHBOR_DISTANCE
            )

            root = Node(ring_def.radius, 0, ring_index)
            self.roots.append(root)
            nodes = []
            nodes.append(root)
            previous = root
            for i in range(1, num_points):
                a = (i / num_points) * math.pi * 2
                node = Node(
                    math.cos(a) * ring_def.radius,
                    math.sin(a) * ring_def.radius,
                    ring_index,
                )
                nodes.append(node)
                previous.set_next(node)
                previous = node
            previous.set_next(root)
            self.rings.append(nodes)

    def insert_node(self):
        for ring_index, nodes in enumerate(self.rings):
            ring_def = self.ring_defs[ring_index]
            if random.random() < ring_def.growth_rate:
                insert_index = random.randint(1, len(nodes) - 1)
                prev = nodes[insert_index]
                next = prev.next

                node = Node(
                    (prev.pos.x + next.pos.x) * 0.5,
                    (prev.pos.y + next.pos.y) * 0.5,
                    ring_index,
                )
                nodes.insert(insert_index + 1, node)
                prev.set_next(node)
                next.set_prev(node)

    def update(self):
        self.insert_node()

        # for i, node in enumerate(self.nodes):
        #     if self.nodes[(i + 1) % len(self.nodes)] != node.next:
        #         raise Exception

        for nodes in self.rings:
            for node in nodes:
                node.update(self.rings)

        for nodes in self.rings:
            for node in nodes:
                node.pos = node.pos_next
