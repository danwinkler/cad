from solid import *
from solid.utils import *

import prettytable
import binpacking
import rectpack


def plan_tstack_orient(s, o):
    l = s.params["size"]
    l.sort()
    l = [l[o["x"]], l[o["y"]], l[o["z"]]]
    s.params["size"] = l
    return s


def plan_tstack_translate(s, o):
    return translate([o["x"], o["y"], o["z"]])(s)


def plan_tstack_scale(s, o):
    return scale([o["x"], o["y"], o["z"]])(s)


def plan_tstack_rotate(s, o):
    return rotate(a=o["a"], v=o["v"])(s)


def plan_tstack_sub(s, o):
    return difference()(s, o["o"])


def plan_tstack_minkowski(s, o):
    return minkowski()(s, o["o"])


plan_tstack_fns = {
    "orient": plan_tstack_orient,
    "translate": plan_tstack_translate,
    "scale": plan_tstack_scale,
    "rotate": plan_tstack_rotate,
    "sub": plan_tstack_sub,
    "minkowski": plan_tstack_minkowski,
}


def plan_process_transform_stack(s, stack):
    for t in stack:
        s = plan_tstack_fns[t["type"]](s, t)
    return s


class Primitive:
    pass


class Cube(Primitive):
    def __init__(self, x, y, z):
        self.solid = cube([x, y, z])


class Cylinder(Primitive):
    def __init__(self, h, r, segments=12):
        self.solid = cylinder(r=r, h=h, segments=segments)


class Sphere(Primitive):
    def __init__(self, r, segments=12):
        self.solid = sphere(r=r, segments=segments)


class Part:
    def p_t_s_set(self, a):
        self.__dict__["__plan_transform_stack"] = a

    def p_t_s_get(self):
        if not hasattr(self, "__plan_transform_stack"):
            self.p_t_s_set([])
        return self.__dict__["__plan_transform_stack"]

    plan_transform_stack = property(p_t_s_get, p_t_s_set)

    def orient(self, x, y, z):
        self.plan_transform_stack.append({"type": "orient", "x": x, "y": y, "z": z})
        return self

    def translate(self, x, y, z):
        self.plan_transform_stack.append({"type": "translate", "x": x, "y": y, "z": z})
        return self

    def scale(self, x, y=None, z=None):
        if y == None:
            y = x
        if z == None:
            z = x
        self.plan_transform_stack.append({"type": "scale", "x": x, "y": y, "z": z})
        return self

    def flipx(self):
        self.plan_transform_stack.append({"type": "scale", "x": -1, "y": 1, "z": 1})
        return self

    def flipy(self):
        self.plan_transform_stack.append({"type": "scale", "x": 1, "y": -1, "z": 1})
        return self

    def flipz(self):
        self.plan_transform_stack.append({"type": "scale", "x": 1, "y": 1, "z": -1})
        return self

    def rotate(self, a=0, v=[0, 0, 1]):
        self.plan_transform_stack.append({"type": "rotate", "a": a, "v": v})
        return self

    def cut(self, o):
        self.plan_transform_stack.append({"type": "sub", "o": o.get_solid()})
        return self

    def minkowski(self, o):
        self.plan_transform_stack.append({"type": "minkowski", "o": o.get_solid()})
        return self

    def get_solid(self):
        part = []
        attrs = dir(self)
        for attr_name in attrs:
            attr = getattr(self, attr_name)
            if isinstance(attr, Part):
                part.append(attr.get_solid())
            elif isinstance(attr, Primitive):
                part.append(attr.solid)
        if len(part) == 1:
            part = part[0]
        if len(self.plan_transform_stack) == 0:
            return part
        return plan_process_transform_stack(part, self.plan_transform_stack)

    def render(self, filename):
        s = self.get_solid()
        with open(filename, "w") as f:
            f.write(scad_render(union()(s)))

    def get_bom_parts(self):
        parts = []

        def build_bom(p):
            try:
                info = p.bom_info()
                parts.append(info)
            except AttributeError:
                pass  # p doesn't define bom_info, don't worry about it

            attrs = dir(p)
            for attr_name in attrs:
                attr = getattr(p, attr_name)
                if isinstance(attr, Part):
                    build_bom(attr)

        build_bom(self)

        return parts

    def binpack_1d(self, t, *args, **kwargs):
        if isinstance(t, type):
            t = t.__name__

        values = []

        key = list(kwargs.keys())[0]

        parts = self.get_bom_parts()

        for v in parts:
            if v["type"] == t:
                values += [v[key]]

        if len(values) == 0:
            return []

        return binpacking.to_constant_volume(values, kwargs[key])

    def binpack_2d(self, t, *args, **kwargs):
        if isinstance(t, type):
            t = t.__name__

        rects = []

        a = list(kwargs.keys())[0]
        b = list(kwargs.keys())[1]

        parts = self.get_bom_parts()

        for v in parts:
            if v["type"] == t:
                rects += [(rectpack.float2dec(v[a], 3), rectpack.float2dec(v[b], 3))]

        packer = rectpack.newPacker()

        for r in rects:
            packer.add_rect(*r)

        packer.add_bin(kwargs[a], kwargs[b], count=float("inf"))

        packer.pack()

        return packer

    def bill_of_materials(self):
        parts = self.get_bom_parts()

        table_dict = {}
        columns = ["key", "type", "length", "width"]

        for part in parts:
            key = part["key"]
            if key not in table_dict:
                d = {"count": 0}
                for c in columns:
                    d[c] = part.get(c, "")
                table_dict[key] = d
            table_dict[key]["count"] += 1

        columns += ["count"]
        table = prettytable.PrettyTable(field_names=columns)

        for k, v in table_dict.items():
            table.add_row([v[n] for n in columns])

        return table.get_string()


class Board(Part):
    short = 1.5
    long = 3.5

    def __init__(self, length):
        self.length = length
        self.part = Cube(length, self.short, self.long)

    def bom_info(self):
        return {
            "key": str(self.short) + "x" + str(self.long) + "x" + str(self.length),
            "type": self.__class__.__name__,
            "bin": ["length"],
            "length": self.length,
        }


class Panel(Part):
    thickness = 0.5

    def __init__(self, width, length, thickness=None):
        self.width = width
        self.length = length

        if thickness:
            self.thickness = thickness

        self.part = Cube(width, length, self.thickness)

    def bom_info(self):
        return {
            "key": str(self.width) + "x" + str(self.length) + "x" + str(self.thickness),
            "type": self.__class__.__name__,
            "bin": ["width", "length"],
            "width": self.width,
            "length": self.length,
        }


class Rod(Part):
    def __init__(self, r, h, segments=12):
        self.r = r
        self.h = h
        self.part = Cylinder(r=r, h=h, segments=segments)


class CubePart(Part):
    def __init__(self, x, y, z):
        self.cube = Cube(x, y, z)


class SpherePart(Part):
    def __init__(self, r, segments=12):
        self.sphere = Sphere(r, segments)


class Box(Part):
    def __init__(
        self,
        width,
        length,
        height,
        bottom=1,
        left=1,
        right=1,
        front=1,
        back=1,
        top=1,
        thickness=None,
        roundover=None,
        roundoversegments=12,
    ):
        if thickness:
            bottom = left = right = front = back = top = thickness

        self.width = width
        self.length = length
        self.height = height

        self.bottom = bottom
        self.left = left
        self.right = right
        self.front = front
        self.back = back
        self.top = top

        boxwidth = width
        boxlength = length
        boxheight = height

        if top == 0:
            top = -1
            if roundover:
                boxheight += roundover

        if bottom == 0:
            bottom = -1
        if left == 0:
            left = -1
        if right == 0:
            right = -1
        if front == 0:
            front = -1
        if back == 0:
            back = -1

        if roundover:
            boxwidth -= roundover * 2
            boxlength -= roundover * 2
            boxheight -= roundover * 2

        self.box = CubePart(boxwidth, boxlength, boxheight)

        if roundover:
            self.box.translate(roundover, roundover, roundover)
            self.box.minkowski(SpherePart(roundover, roundoversegments))

            if top <= 0:
                self.box.cut(
                    CubePart(width, length, roundover + 1).translate(0, 0, height)
                )

        self.box.cut(
            CubePart(
                width - (left + right), length - (front + back), height - (top + bottom)
            ).translate(left, front, bottom)
        )

    def inner_corner(self, x, y, z):
        rx = self.left if x == 0 else self.width - self.right
        ry = self.front if y == 0 else self.length - self.back
        rz = self.bottom if z == 0 else self.height - self.top
        return rx, ry, rz

    def place_in_corner(self, o, x, y, z):
        if x == 1:
            o.flipx()
        if y == 1:
            o.flipy()
        if z == 1:
            o.flipz()
        return o.translate(*self.inner_corner(x, y, z))
