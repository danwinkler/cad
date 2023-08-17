from solid import *
from solid.utils import *

from cad.common.helper import *
from cad.common.plan import *

mm_to_in = 25.4

# Cart variables
platform_width = 26
cart_width = platform_width + 1.5 * 2
cart_depth = 24
cart_height = 36
shelf_height_above_ground = 4
miter_platform_height = 5
wing_width = 24
wing_tongue_length = 18
wing_tongue_thickness = 0.75

wing_lifted = False


# Wood primitives
class W2x4(Board):
    short = 1.5
    long = 3.5


class W2x6(Board):
    short = 1.5
    long = 5.5


class WingWood(Board):
    short = 0.75
    long = 4


class Plywood(Panel):
    thickness = 0.5


class WingTongueBoard(Panel):
    thickness = wing_tongue_thickness


# Cart pieces
class BottomShelf(Part):
    width = cart_width - W2x4.short * 4
    depth = cart_depth - W2x4.short * 4

    front = W2x4(width)
    back = W2x4(width).translate(0, depth - W2x4.short, 0)
    left = W2x4(depth - W2x4.short * 2).orient(0, 2, 1).translate(0, W2x4.short, 0)
    right = (
        W2x4(depth - W2x4.short * 2)
        .orient(0, 2, 1)
        .translate(width - W2x4.short, W2x4.short, 0)
    )
    platform = Plywood(width, depth).translate(0, 0, W2x4.long)


class Leg(Part):
    length = cart_height - shelf_height_above_ground - 0.5

    b = W2x6(length).orient(1, 0, 2).translate(-wing_tongue_thickness, 0, 0)
    a = W2x4(length).orient(0, 1, 2).translate(0, b.short, 0)
    bottom = (
        W2x6(W2x6.long)
        .orient(1, 2, 0)
        .translate(-wing_tongue_thickness, 0, -W2x6.short)
    )


class Rim(Part):
    wing_slot_thickness = wing_tongue_thickness

    front = W2x4(cart_width + wing_slot_thickness * 2).translate(
        -wing_slot_thickness, 0, 0
    )
    back = W2x4(cart_width + wing_slot_thickness * 2).translate(
        -wing_slot_thickness, cart_depth - W2x4.short, 0
    )
    left = (
        W2x4(cart_depth - W2x4.short * 2)
        .orient(0, 2, 1)
        .translate(-wing_slot_thickness, W2x4.short, 0)
    )
    right = (
        W2x4(cart_depth - W2x4.short * 2)
        .orient(0, 2, 1)
        .translate(cart_width + wing_slot_thickness - W2x4.short, W2x4.short, 0)
    )


class WingPlatform(Part):
    front = WingWood(wing_width)
    back = WingWood(wing_width).translate(0, cart_depth - WingWood.short, 0)
    left = (
        WingWood(cart_depth - WingWood.short * 2)
        .orient(0, 2, 1)
        .translate(0, WingWood.short, 0)
    )
    right = (
        WingWood(cart_depth - WingWood.short * 2)
        .orient(0, 2, 1)
        .translate(wing_width - WingWood.short, WingWood.short, 0)
    )
    platform = Plywood(wing_width, cart_depth).translate(0, 0, WingWood.long)
    support_pos = (wing_width) * 0.5 + 2
    support_a = (
        WingWood(cart_depth - WingWood.short * 2)
        .orient(1, 2, 0)
        .translate(support_pos - WingWood.long * 0.5, WingWood.short, 0)
    )
    screw_length = W2x4.long + (miter_platform_height - WingWood.long)
    support_screw = Rod(r=0.2, h=screw_length).translate(
        support_pos, cart_depth * 0.5, -screw_length
    )


class Wing(Part):
    tongue = WingTongueBoard(
        cart_depth - W2x4.short * 2 - W2x6.short * 2, wing_tongue_length
    )
    tongue.orient(0, 2, 1).translate(
        0, W2x4.short + W2x6.short, -wing_tongue_length + W2x4.long - 0.5
    )

    tongue_attachment = (
        W2x4(cart_depth).orient(0, 2, 1).translate(wing_tongue_thickness, 0, -0.5)
    )

    platform_height = miter_platform_height - WingWood.long

    tongue.cut(
        Rod(r=1, h=10)
        .rotate(v=[0, 1, 0], a=90)
        .translate(-1, cart_depth * 0.5, -WingPlatform.support_pos + platform_height)
    )

    def __init__(self, angle=0):
        self.platform = (
            WingPlatform()
            .rotate(a=angle, v=[0, 1, 0])
            .translate(W2x4.short + wing_tongue_thickness, 0, self.platform_height)
        )


class WingSupport(Part):
    tongue_support_height = 2
    tongue_support = WingTongueBoard(
        cart_depth - W2x4.short * 2 - W2x6.short * 2, tongue_support_height
    )
    tongue_support.orient(0, 2, 1).translate(
        0,
        W2x4.short + W2x6.short,
        -wing_tongue_length + W2x4.long - 0.5 - tongue_support_height,
    )

    wing_height = 24
    wing_depth = cart_depth - W2x4.short * 2
    wing_angle = 0
    wing = WingTongueBoard(wing_depth, wing_height)
    wing.orient(0, 1, 2)
    wing.rotate(a=-wing_angle, v=[0, 0, 1])
    wing.translate(wing_tongue_thickness, W2x6.short, -W2x4.long - wing_height - 0.5)
    # This hole is only visible when the wing is in, because im lazy
    wing.cut(
        Rod(r=1, h=10)
        .rotate(v=[0, 1, 0], a=90)
        .translate(
            -1, cart_depth * 0.5, -WingPlatform.support_pos + Wing.platform_height
        )
    )


class Table(Part):
    b_shelf = BottomShelf().translate(
        W2x4.short * 2, W2x4.short * 2, shelf_height_above_ground
    )

    l0 = Leg().translate(W2x4.short, W2x4.short, shelf_height_above_ground)
    l1 = (
        Leg()
        .flipx()
        .translate(cart_width - W2x4.short, W2x4.short, shelf_height_above_ground)
    )
    l2 = (
        Leg()
        .flipy()
        .translate(W2x4.short, cart_depth - W2x4.short, shelf_height_above_ground)
    )
    l3 = (
        Leg()
        .flipx()
        .flipy()
        .translate(
            cart_width - W2x4.short, cart_depth - W2x4.short, shelf_height_above_ground
        )
    )

    rim = Rim().translate(0, 0, cart_height - W2x4.long - 0.5)

    platform = Plywood(platform_width, cart_depth).translate(
        (cart_width - platform_width) * 0.5, 0, cart_height - 0.5
    )

    wing_a = Wing(0).translate(cart_width - 1.5, 0, cart_height)
    wing_b = Wing(0).flipx().translate(1.5, 0, cart_height)

    wing_support_a = WingSupport().translate(cart_width - 1.5, 0, cart_height)
    wing_support_b = WingSupport().flipx().translate(1.5, 0, cart_height)


t = Table().scale(mm_to_in)

print(t.bill_of_materials())

pack2x4 = t.binpack_1d(W2x4, length=8 * 12)
pack2x6 = t.binpack_1d(W2x6, length=8 * 12)
packWingWood = t.binpack_1d(WingWood, length=8 * 12)
packPlywood = t.binpack_2d(Plywood, width=4 * 12, length=8 * 12)
packWingTongueBoard = t.binpack_2d(WingTongueBoard, width=4 * 12, length=8 * 12)

print("Pack 2x4 - " + str(len(pack2x4)))
print(pack2x4)

print("Pack 2x6 - " + str(len(pack2x6)))
print(pack2x6)

print("Pack Wing Wood - " + str(len(packWingWood)))
print(packWingWood)

print("Pack Wing Board - " + str(len(packWingTongueBoard)))

print("pack Plywood - " + str(len(packPlywood)))

t.render(__file__ + ".scad")
