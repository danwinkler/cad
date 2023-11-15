class EditorPacket:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class ExtrudedModel:
    def __init__(self, shape, thickness, orientation_fn):
        self.shape = shape
        self.thickness = thickness
        self.orientation_fn = orientation_fn
