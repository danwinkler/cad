import math
import random

from solid import *
from solid.utils import *

from cad.common.helper import *

# Hole center is 12 mm from base and is 1.5mm radius

inches_in_mm = 25.4
half_in = inches_in_mm / 2.0

hole_depth = 25
connector_length = 45
size = half_in + 0.5
rad = size / 2
wall_thickness = 3

parts = []


# Try to find 2 vectors that are completely clear on one side, prefering one with the largest angle
def find_2_sided_downvec(vec_list):
    exclude_list = []
    while True:  # while we havent found the vector we want
        big_vec = None
        big_angle = 0
        for i in range(len(vec_list)):
            for j in range(
                i + 1, len(vec_list)
            ):  # start at i+1 so that we don't test i,j if we've already tested j,i
                if i == j:
                    continue
                if (i, j) in exclude_list:
                    continue

                angle = math.acos(vec_list[i].dot(vec_list[j]))
                if angle > big_angle:
                    big_vec = (i, j)
                    big_angle = angle

        # If big_vec == None, we failed to find a flat spot between two vectors
        if big_vec == None:
            return False, False

        # Check for vectors on either side, if one side is clear, that's our side
        def is_clear(vec):
            for i in range(len(vec_list)):
                if i in big_vec:
                    continue
                # angle needs to be >90 (math.pi/2) to make sure its on the other side
                angle = math.acos(vec.dot(vec_list[i]))
                if angle < math.pi / 2:
                    return False
            return True

        cross = vec_list[big_vec[0]].cross(vec_list[big_vec[1]])
        if is_clear(cross):
            return True, cross

        # Try other side...
        cross *= -1
        if is_clear(cross):
            return True, cross

        # Welp this pair is bad, add to exclude_list and try again
        exclude_list.append(big_vec)


def triangle_intersection(v1, v2, v3, o, d):
    EPSILON = 0.000001
    # Find vectors for two edges sharing V1
    e1 = v2 - v1
    e2 = v3 - v1
    # Begin calculating determinant - also used to calculate u parameter
    p = d.cross(e2)
    # if determinant is near zero, ray lies in plane of triangle
    det = e1.dot(p)
    # NOT CULLING
    if det > -EPSILON and det < EPSILON:
        return False
    inv_det = 1.0 / det

    # calculate distance from V1 to ray origin
    t = o - v1

    # Calculate u parameter and test bound
    u = t.dot(p) * inv_det
    # The intersection lies outside of the triangle
    if u < 0.0 or u > 1.0:
        return False

    # Prepare to test v parameter
    q = t.cross(e1)

    # Calculate V parameter and test bound
    v = d.dot(q) * inv_det
    # The intersection lies outside of the triangle
    if v < 0.0 or u + v > 1.0:
        return False

    t = e2.dot(q) * inv_det

    if t > EPSILON:
        return True

    return False


def find_3_sided_downvec(vec_list):
    big_down = None
    big_size = 0
    big_shift = 0
    for i in range(len(vec_list)):
        for j in range(len(vec_list)):
            if j == i:
                continue
            for k in range(len(vec_list)):
                if k == i or k == j:
                    continue

                v_a = vec_list[j] - vec_list[i]
                v_b = vec_list[k] - vec_list[i]
                v_c = v_a - v_b

                # Check to make sure nobody else is inside triangle
                good = True
                for l in range(len(vec_list)):
                    if l in (i, j, k):
                        continue

                    hit = triangle_intersection(
                        vec_list[i], vec_list[j], vec_list[k], Vec3(), vec_list[l]
                    )
                    if hit:
                        good = False
                        break

                if good:
                    # TODO: make this score like the area of the triangle
                    score = v_a.length() + v_b.length() + v_c.length()
                    if score > big_size:
                        big_size = score
                        v_b.normalize()
                        v_a.normalize()

                        big_down = v_b.cross(v_a)
                        big_down.normalize()
                        if (
                            big_down.dot(vec_list[i]) < 0
                        ):  # Use the dot to figure out which side I think..
                            big_down *= -1

    if big_down != None:
        return True, big_down
    return False, False


def rotate_to(vec, down_vec):
    vec = vec.copy()
    orig_down = Vec3(0.0000001, 0.0000001, -1).normalize()
    axis = orig_down.cross(down_vec)
    dot = orig_down.dot(down_vec)
    angle = math.acos(dot)
    dot2 = abs(dot) > 0.5
    if dot > 0 and dot2:
        angle *= -1
    if dot > 0 and not dot2:
        angle *= -1
    if dot < 0 and dot2:
        angle *= -1
    if dot < 0 and not dot2:
        angle *= -1
    return vec.rotate(axis, angle).normalize()


def build_connector(vec_list, offset):
    connector = []
    flats = []
    holes = []
    sph = sphere(connector_length)

    for vec in vec_list:
        connector.append(
            rot_on_vec(vec, cylinder(r=rad + wall_thickness, h=connector_length))
        )
        holes.append(
            rot_on_vec(
                vec,
                up(connector_length - hole_depth)(cylinder(r=rad, h=connector_length)),
            )
        )
        flat_angle = -math.degrees(math.atan2(-vec.y, vec.x))
        length = Vec3(vec.x, vec.y, 0).length()
        flats.append(
            rotate(v=[0, 0, 1], a=flat_angle)(
                translate([0, -rad, 0])(cube([connector_length * length, size, 1]))
            )
        )

    part = hull()(connector)  # We hull all of the cylinders
    part = intersection()(
        part, sph
    )  # then we intersect with a sphere to round the ends
    part = up(offset)(part)  # Shift the part up in prep for the flat hull
    part = hull()(
        union()(flats) + part
    )  # We hull with the flat pieces on the xy axis to print easily
    part -= up(offset)(
        holes
    )  # cut the holes, shifted up because we already shifted the part
    part -= translate([-100, -100, -100])(
        cube([200, 200, 100])
    )  # in case theres a little bit below ground, cut it off

    return part


def connector_redux(vec_list):
    vec_list = vec_list = [v.copy().normalize() for v in vec_list]

    # Try to find a flat spot make by the sides two vectors (Triangle is [origin, v1, v2])
    found, down_vec = find_2_sided_downvec(vec_list)

    # If that doesn't exist, find a flat spot make from the ends of 3 vectors (triangle is [v1, v2, v3])
    if not found:
        found, down_vec = find_3_sided_downvec(vec_list)

    down_vec.normalize()

    # This should never happen
    if not found:
        print("Couldn't find downvec")

    # Rotate all vectors so that the flat spot we found is pointed straight down
    vec_list = [rotate_to(v, down_vec) for v in vec_list]

    # Find the offset (some vectors will be z<0, so we need to make sure to shift up so that everything is flat with the build plate)
    offset = 1000
    for vec in vec_list:
        if vec.z < offset:
            offset = vec.z

    # This is some crappy code that trys to account for the length/width of the connector
    offset *= connector_length
    offset -= rad + 3
    offset *= -1

    orig_down = Vec3(
        0.0000001, 0.0000001, -1
    ).normalize()  # cross product gets all kind of fucked if both are on same axis plane
    axis = orig_down.cross(down_vec)
    dot = orig_down.dot(down_vec)

    return build_connector(
        vec_list, offset
    )  # + rot_on_vec( down_vec, cylinder(r=1, h=100) )
