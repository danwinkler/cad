import random

from noise import pnoise2 as noise
from solid import *
from solid.utils import *

parts = []

random.seed(4)

width = 100
length = 100

border_size = 2
base_thickness = 2

support_size = 4
support_sep = 8
support_height = 1.5

support_num_x = ((width - support_size) / (support_size + support_sep)) + 1
support_num_y = ((length - support_size) / (support_size + support_sep)) + 1

city_x = 10
city_y = 10

city_width = (width - (border_size * 4)) / city_x
city_length = (length - (border_size * 4)) / city_y

building_min_height = 3
building_max_height = 10

for x in range(support_num_x):
    for y in range(support_num_y):
        parts.append(
            translate(
                [x * (support_size + support_sep), y * (support_size + support_sep), 0]
            )(cube([support_size, support_size, support_height]))
        )

for x in range(support_num_x):
    parts.append(
        translate([x * (support_size + support_sep), 0, support_height - 0.5])(
            cube([support_size, length, 0.5])
        )
    )

for y in range(support_num_y):
    parts.append(
        translate([0, y * (support_size + support_sep), support_height - 0.5])(
            cube([width, support_size, 0.5])
        )
    )


parts.append(up(support_height)(cube([width, length, base_thickness])))

parts.append(
    translate([0, 0, support_height + base_thickness])(
        cube([width, border_size, base_thickness])
    )
)
parts.append(
    translate([0, 0, support_height + base_thickness])(
        cube([border_size, length, base_thickness])
    )
)
parts.append(
    translate([0, length - border_size, support_height + base_thickness])(
        cube([width, border_size, base_thickness])
    )
)
parts.append(
    translate([width - border_size, 0, support_height + base_thickness])(
        cube([border_size, length, base_thickness])
    )
)

heights = []

for x in range(city_x):
    height_row = []
    for y in range(city_y):
        x_diff = (x + 0.5) - (city_x / 2.0)
        y_diff = (y + 0.5) - (city_y / 2.0)
        dist_from_center = x_diff**2 + y_diff**2
        height_mult = 0.8 / ((dist_from_center + 4) * 0.03)
        height = height_mult * random.uniform(building_min_height, building_max_height)
        height_row.append(height)
        parts.append(
            translate(
                [
                    border_size * 2 + x * city_width,
                    border_size * 2 + y * city_length,
                    support_height + base_thickness,
                ]
            )(cube([city_width - 0.001, city_length - 0.001, height]))
        )
    heights.append(height_row)

for x in range(0, city_x, 2):
    for y in range(0, city_y, 2):
        height_min = 100
        for xx in range(0, city_x, 1):
            for yy in range(0, city_y, 1):
                if heights[xx][yy] < height_min:
                    height_min = heights[xx][yy]
        parts.append(
            translate(
                [
                    border_size * 2 + x * city_width,
                    border_size * 2 + y * city_length,
                    support_height + base_thickness,
                ]
            )(cube([city_width * 2 + 0.001, city_length * 2 + 0.001, height_min]))
        )

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(scad_render(union()(parts)))
