import pathlib

import solid

from cad.projects.y2024.tea_shelves.box import BoxA


def in_to_mm(inches):
    return inches * 25.4


def holder_model():
    box_inst = BoxA()
    box_inst.depth = 300
    box_inst.width = 240
    box_inst.length = 80
    box_inst.y_segments = 1
    box_inst.has_lid = False
    box_inst.has_bottom = True

    return box_inst.get_model()


model = holder_model()
model.n_bins = 2

output_dir = pathlib.Path(__file__).parent / (pathlib.Path(__file__).stem + "_parts")
model.render_parts(output_dir)
# model.render_single_dxf(output_dir / "single.dxf")

top_level_geom = model.render_scad()

print(f"Total Cut Length: {model.get_total_cut_length()}")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
