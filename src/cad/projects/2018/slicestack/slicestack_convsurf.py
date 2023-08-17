import pathlib
import pickle
import random

from tqdm import tqdm

from cad.common.convolution_surface import ConvolutionSurface

from .differential_line import DiffLine, NodeData

df = DiffLine()
df.init_circle()

layers = []
points_per_layer = 300
height = 710
flip = False
cache_file = pathlib.Path("sim_{}.pickle".format(height))

if cache_file.exists():
    with open(cache_file, "rb") as f:
        layers = pickle.load(f)
else:
    print("Running Simulation")
    for i in tqdm(range(height)):
        df.update()

        if i % 1 == 0:
            layer = []
            for ring in df.rings:
                ring_layer = []
                for n in ring:
                    nd = NodeData(n)
                    if flip:
                        nd.pos.z = height - i
                    else:
                        nd.pos.z = i
                    ring_layer.append(nd)
                layer.append(ring_layer)
            layers.append(layer)
    with open(cache_file, "wb") as f:
        pickle.dump(layers, f)

layers = layers[:100]

surface = ConvolutionSurface(3, 0.8)

# Scale
for li, layer in enumerate(layers):
    for ring in layer:
        for ni, nd in enumerate(ring):
            nd.pos.z *= 0.5


def get_node_index_from_layer(layer, node_id):
    return [i for i, n in enumerate(layer) if n.id == node_id][0]


def build_angled_line(start_index, direction, angle):
    last_node = None
    last_pos = None
    for li, layer in enumerate(layers):
        layer = layer[0]
        if last_node is None:
            last_node = layer[start_index]
            last_pos = last_node.pos
        else:
            node_index = get_node_index_from_layer(layer, last_node.id)
            next_node_index = (node_index + direction + len(layer)) % len(layer)

            node = layer[node_index]
            next_node = layer[next_node_index]

            lerp_amount = float(li % angle) / angle

            pos = node.pos.lerp(next_node.pos, lerp_amount)

            surface.add_line(last_pos.to_list(), pos.to_list(), 1.8)
            last_pos = pos
            last_node = next_node if li % angle == 0 else node


for i in range(len(layers[0][0])):
    build_angled_line(i, 1 if i % 2 == 0 else -1, 3)

"""
for li, layer in enumerate(layers[:10]):
    layer = layer[0]
    for ni, nd in enumerate(layer):
        surface.add_line(
            nd.pos.to_list(),
            layer[(ni+1) % len(layer)].pos.to_list(),
            1.8
        )

        random.seed( li * 1000 + ni )
        if li+1 < len(layers) and random.random() > .6:
            surface.add_line(
                nd.pos.to_list(),
                [l for l in layers[li+1][0] if l.id == nd.id][0].pos.to_list(),
                2
            )
"""
surface.render()
