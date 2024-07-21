import math
import random

import pymunk
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from tqdm import tqdm

from cad.common.lasercut import Model, MultipartModel


def pack_polygons(polys, n_steps=10000, delta_time=0.01, gravity=(-100, 0), margin=1):
    body_to_shapely = {}

    rows = 3

    space = pymunk.Space()
    space.gravity = gravity

    walls = [(-100, -100, 100, 2000), (-100, -100, 2000, 100), (-100, 280, 2000, 100)]
    rows = 5
    for wall in walls:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # Shape is a AA box, where wall is x, y, width, height
        shape = pymunk.Poly.create_box(body, size=(wall[2], wall[3]))
        body.position = wall[0] + wall[2] / 2, wall[1] + wall[3] / 2
        shape.elasticity = 1
        shape.friction = 0.1
        space.add(body, shape)

    for i, poly in enumerate(polys):
        body = pymunk.Body()
        body.position = i // rows * 50 + 25, i % rows * 50 + 25
        body.center_of_gravity = (poly.centroid.x, poly.centroid.y)
        expanded_poly = poly.buffer(margin)
        shape = pymunk.Poly(
            body, [(p[0], p[1]) for p in expanded_poly.exterior.coords[:-1]], radius=0.0
        )
        shape.mass = 1
        shape.friction = 0.1
        space.add(body, shape)
        body_to_shapely[body] = poly

    for i in tqdm(range(n_steps)):
        space.step(delta_time)

        if i % 50 == 0:
            # Check to see if all bodies are sleeping
            if all([body.is_sleeping for body in space.bodies]):
                break

    transform_map = {}

    for body, poly in body_to_shapely.items():
        transform_map[poly] = body.position, math.degrees(body.angle)
        # transformed_poly = rotate(poly, math.degrees(body.angle), origin=(0, 0))
        # transformed_poly = translate(
        #     transformed_poly, xoff=body.position.x, yoff=body.position.y
        # )

    return transform_map


def generate_layout(model: MultipartModel):
    layout = {}

    pack_polys = []
    pack_poly_to_model = {}

    for i, m in enumerate(model.models):
        if not isinstance(m, Model):
            continue

        if len(m.parts) == 0:
            continue

        parts = []
        for part in m.parts:
            parts.append(part.polygon)

        unioned = unary_union(parts)
        pack_polys.append(unioned)
        pack_poly_to_model[unioned] = m

    transform_map = pack_polygons(pack_polys)

    for poly, (pos, angle) in transform_map.items():
        m = pack_poly_to_model[poly]
        layout[m] = pos.x + m.minx, pos.y + m.miny, angle

    return layout
