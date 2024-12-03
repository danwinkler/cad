import platform

import numpy as np
import pytest


def is_geometry_water_tight(vertices, triangles):
    """
    Checks if the geometry is watertight by ensuring every edge is shared by exactly two triangles.
    """
    edge_count = {}
    for tri in triangles:
        edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
        for edge in edges:
            sorted_edge = tuple(sorted(edge))
            if sorted_edge in edge_count:
                edge_count[sorted_edge] += 1
            else:
                edge_count[sorted_edge] = 1

    # A watertight mesh should have all edges shared exactly twice
    return all(count == 2 for count in edge_count.values())


@pytest.mark.skipif(
    platform.system() == "Darwin", reason="CUDA is not supported on macOS"
)
@pytest.mark.llmgenerated
def test_convsurf_basic():
    """
    Test ConvSurf basic functionality by creating an object, adding primitives, and generating geometry.
    """
    # Defer import to here as this import will fail on mac
    from cad.common.pyconvsurf import ConvSurf

    # Create ConvSurf object
    conv_surf = ConvSurf(margin=30, resolution=5)

    # Add primitives
    conv_surf.add_line([0, 0, 0], [100, 100, 100], s=1.1)
    conv_surf.add_triangle([0, 0, 0], [100, 0, 0], [0, 100, 0], s=1.1)
    conv_surf.add_rect([0, 0, 0], [100, 0, 0], [100, 100, 0], [0, 100, 0], s=1.1)

    # Generate geometry
    vertices, triangles = conv_surf.generate(isovalue=0.005)

    # Basic assertions
    assert vertices is not None, "Vertices should not be None"
    assert triangles is not None, "Triangles should not be None"
    assert len(vertices) > 0, "Vertices should contain points"
    assert len(triangles) > 0, "Triangles should contain indices"

    # Extra credit: Check for water-tightness
    assert is_geometry_water_tight(vertices, triangles), "Geometry is not watertight"
