from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Transform:
    """Simple 4x4 transform wrapper.

    Immutable; composition returns a new instance.
    """

    matrix: np.ndarray

    @staticmethod
    def identity() -> "Transform":
        return Transform(np.eye(4))

    @staticmethod
    def at(x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0, scale=1.0) -> "Transform":
        sx = np.sin(np.radians(rx))
        cx = np.cos(np.radians(rx))
        sy = np.sin(np.radians(ry))
        cy = np.cos(np.radians(ry))
        sz = np.sin(np.radians(rz))
        cz = np.cos(np.radians(rz))

        rot_x = np.array([[1, 0, 0, 0], [0, cx, -sx, 0], [0, sx, cx, 0], [0, 0, 0, 1]])
        rot_y = np.array([[cy, 0, sy, 0], [0, 1, 0, 0], [-sy, 0, cy, 0], [0, 0, 0, 1]])
        rot_z = np.array([[cz, -sz, 0, 0], [sz, cz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        scale_m = np.diag([scale, scale, scale, 1])

        mat = rot_z @ rot_y @ rot_x @ scale_m
        mat[:3, 3] = [x, y, z]
        return Transform(mat)

    def compose(self, other: "Transform") -> "Transform":
        return Transform(self.matrix @ other.matrix)

    def to_json(self):
        return self.matrix.tolist()
