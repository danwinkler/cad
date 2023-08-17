import math
import random
import time

import connector as conn
from solid import *
from solid.utils import *

from cad.common.helper import *

stick_offset = 20 + 20


def create_vase(model, save_name, base_height=0):
    layers_outer = model.get_layers()
    layers_inner = model.get_layers(shrink_offset=25)

    def outer_fun(h, s):
        return layers_outer[h][s].to_list()

    def inner_fun(h, s):
        return layers_inner[h][s].to_list()

    part = make_trunk(model.height, model.sections, outer_fun, True)
    sub = make_trunk(model.height, model.sections, inner_fun, True)
    if base_height > 0:
        sub -= cylinder(r=1000, h=base_height)
    part -= sub

    if save_name:
        directory = "vase/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + "/" + save_name + ".scad", "w") as f:
            f.write(scad_render(part))

    return part


def create_from_layers_stick_list(layers, save_name):
    sticks = []
    for i in range(len(layers)):
        layer = layers[i]
        for j in range(len(layer)):
            p = layer[j]
            if not p:
                continue

            # To next point on layer
            p_next = layer[(j + 1) % len(layer)]
            if p_next:
                next_vec = p_next.copy()
                next_vec -= p
                sticks.append(next_vec.length())

        for j in range(len(layer)):
            p = layer[j]
            if not p:
                continue

            # To previous point above
            if i + 1 < len(layers):
                p_prev_above = layers[i + 1][(j - 1 if j > 0 else len(layer) - 1)]
                if p_prev_above:
                    prev_above_vec = p_prev_above.copy()
                    prev_above_vec -= p
                    sticks.append(prev_above_vec.length())

            # To point above on next layer
            if i + 1 < len(layers):
                p_above = layers[i + 1][j]
                if p_above:
                    above_vec = p_above.copy()
                    above_vec -= p
                    sticks.append(above_vec.length())

    sticks = [l - stick_offset for l in sticks]
    stick_list = [
        str(i) + " " + str(l) + " " + str(l * 0.0393701) for i, l in enumerate(sticks)
    ]
    # stick_list.sort()
    stick_list = "\n".join(stick_list)

    directory = "designs/" + save_name

    with open(directory + ".txt", "w") as f:
        f.write(stick_list)


def create_from_layers(layers, save_name=None):
    parts = []
    connectors = []
    for i in range(len(layers)):
        layer = layers[i]
        for j in range(len(layer)):
            p = layer[j]
            if not p:
                continue
            connector = []

            # To next point on layer
            p_next = layer[(j + 1) % len(layer)]
            next_vec = p_next.copy()
            next_vec -= p
            parts.append(translate(p.to_list())(cyl_on_vec(next_vec, r=10)))
            connector.append(next_vec)

            # To previous point on layer (don't render)
            p_prev = layer[(j - 1 if j > 0 else len(layer) - 1)]
            prev_vec = p_prev.copy()
            prev_vec -= p
            connector.append(prev_vec)

            # To point above on next layer
            if i + 1 < len(layers):
                p_above = layers[i + 1][j]
                above_vec = p_above.copy()
                above_vec -= p
                parts.append(translate(p.to_list())(cyl_on_vec(above_vec, r=10)))
                connector.append(above_vec)

            # To previous point above (Don't render)
            if i + 1 < len(layers):
                p_prev_above = layers[i + 1][(j - 1 if j > 0 else len(layer) - 1)]
                prev_above_vec = p_prev_above.copy()
                prev_above_vec -= p
                connector.append(prev_above_vec)

            # To next point on lower layer
            if i > 0:
                p_next_below = layers[i - 1][(j + 1) % len(layer)]
                next_below_vec = p_next_below.copy()
                next_below_vec -= p
                parts.append(translate(p.to_list())(cyl_on_vec(next_below_vec, r=10)))
                connector.append(next_below_vec)

            # To point below (Don't render)
            if i > 0:
                p_below = layers[i - 1][j]
                below_vec = p_below.copy()
                below_vec -= p
                connector.append(below_vec)

            parts.append(translate(p.to_list())(sphere(30)))
            connectors.append(connector)

    if save_name:
        directory = "designs/" + save_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(len(connectors)):
            with open(directory + "/" + str(i) + ".scad", "w") as f:
                c = conn.connector_redux(connectors[i])
                c -= up(2)(
                    rotate(v=[0, 1, 0], a=180)(
                        linear_extrude(height=3)(
                            text(str(i), size=8, valign="center", halign="center")
                        )
                    )
                )
                f.write(scad_render(c))

    return parts
