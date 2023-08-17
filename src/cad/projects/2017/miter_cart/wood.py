from solid import *
from solid.utils import *

import prettytable

import binpacking
import rectpack

wood_bom_columns = ["name", "count", "type", "width", "length", "thickness"]

wood_bom_table = {}


def wood_bom_update(name, *args, **kwargs):
    if name not in wood_bom_table:
        row = {
            "name": name,
            "count": 0,
            "type": kwargs.get("type", ""),
            "width": kwargs.get("width", ""),
            "length": kwargs.get("length", ""),
            "thickness": kwargs.get("thickness", ""),
        }

        wood_bom_table[name] = row

    wood_bom_table[name]["count"] += 1


def wood(size):
    wood_bom_update("x".join(str(x) for x in size))
    return cube(size)


def wood_2x6(length):
    wood_bom_update("2x6x" + str(length), type="2x6", length=length)
    return cube([length, 1.5, 5.5])


def wood_2x4(length):
    wood_bom_update("2x4x" + str(length), type="2x4", length=length)
    return cube([length, 1.5, 3.5])


def plywood(width, length, thickness=0.5):
    t = "plywood " + str(width) + "x" + str(length) + "x" + str(thickness)
    wood_bom_update(
        t,
        type="plywood-" + str(thickness),
        width=width,
        length=length,
        thickness=thickness,
    )
    return cube([width, length, thickness])


def cube_rot(order):
    def call_fn(c):
        l = c.params["size"]
        l.sort()
        l = [l[order[0]], l[order[1]], l[order[2]]]
        c.params["size"] = l
        return c

    return call_fn


def wood_pack_1d(type, *args, **kwargs):
    values = []

    key = list(kwargs.keys())[0]

    for k, v in wood_bom_table.items():
        if v["type"] == type:
            values += [v[key]] * v["count"]

    return binpacking.to_constant_volume(values, kwargs[key])


def wood_pack_2d(type, *args, **kwargs):
    rects = []

    a = list(kwargs.keys())[0]
    b = list(kwargs.keys())[1]

    for k, v in wood_bom_table.items():
        if v["type"] == type:
            rects += [(rectpack.float2dec(v[a], 3), rectpack.float2dec(v[b], 3))] * v[
                "count"
            ]

    packer = rectpack.newPacker()

    for r in rects:
        packer.add_rect(*r)

    packer.add_bin(kwargs[a], kwargs[b], count=float("inf"))

    packer.pack()

    return packer


def wood_bom():
    table = prettytable.PrettyTable(field_names=wood_bom_columns)

    types = {}

    for k, v in wood_bom_table.items():
        if "type" in v:
            if v["type"] not in types:
                types[v["type"]] = {"length": 0, "width": 0, "type": v["type"]}
            types[v["type"]]["length"] += v["length"] or 0
            types[v["type"]]["width"] += v["width"] or 0
        table.add_row([v[n] for n in wood_bom_columns])

    quantity_cols = ["type", "length", "width"]
    quantity_table = prettytable.PrettyTable(field_names=quantity_cols)

    for k, v in types.items():
        quantity_table.add_row([v[n] for n in quantity_cols])

    return table.get_string() + "\n" + quantity_table.get_string()
