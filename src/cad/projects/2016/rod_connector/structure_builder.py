import sys

from . import layer_structure, structure_list
from .structure_class import *

models = dir(structure_list)
models = filter(lambda x: x[0] != "_", models)
models = [getattr(structure_list, model) for model in models]


def model_filter(m):
    try:
        return m.__module__ in ["structure_list"]
    except:
        return False


models = filter(model_filter, models)


def create_vase(m, offset=0):
    return m.get_object()  # - m.get_object( shrink_offset=30 )


for model in models:
    print("Building: " + model.__name__)
    m = model()
    if issubclass(model, LayerStructure):
        layer_structure.create_vase(m, model.__name__)
    else:
        with open("vase/" + model.__name__ + ".scad", "w") as f:
            f.write(scad_render(create_vase(m)))
        if hasattr(model, "get_list"):
            with open("designs/" + model.__name__ + "_list.txt", "w") as f:
                f.write(m.get_list())
