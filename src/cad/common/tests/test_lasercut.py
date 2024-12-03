import re

import pytest
from shapely.geometry import MultiPolygon, Polygon, box

from cad.common.lasercut import (
    AffineTransformRenderer,
    Model,
    MultipartModel,
    get_text_polygon,
    s_poly_to_scad,
    skeleton_to_polys,
)


@pytest.mark.llmgenerated
class TestLaserCut:
    def test_s_poly_to_scad_single_polygon(self):
        """
        Test conversion of a single polygon to SCAD.
        """
        poly = box(0, 0, 10, 10)
        scad = s_poly_to_scad(poly)
        assert scad is not None, "SCAD object should not be None"
        assert len(scad.children) == 1, "Should have one child in SCAD output"

    def test_s_poly_to_scad_multipolygon(self):
        """
        Test conversion of a MultiPolygon to SCAD.
        """
        poly1 = box(0, 0, 10, 10)
        poly2 = box(20, 20, 30, 30)
        multipoly = MultiPolygon([poly1, poly2])
        scad = s_poly_to_scad(multipoly)
        assert scad is not None, "SCAD object should not be None"
        assert len(scad.children) == 2, "Should have two children in SCAD output"

    def test_skeleton_to_polys(self):
        """
        Test skeleton_to_polys with simple line segments.
        """
        lines = [
            ((0, 0, 500), (10, 0, 500)),
            ((0, 10, 500), (10, 10, 500)),
        ]
        polys = skeleton_to_polys(lines)
        assert len(polys) > 0, "Should generate polygons from skeleton"
        for poly in polys:
            assert isinstance(poly, Polygon), "Generated object should be a Polygon"

    def test_model_add_poly(self):
        """
        Test adding polygons to a Model.
        """
        model = Model()
        poly = box(0, 0, 10, 10)
        renderer = model.add_poly(poly)
        assert len(model.parts) == 1, "Model should contain one part"
        assert model.parts[0].polygon.equals(poly), "Polygon should match input"
        assert isinstance(
            renderer, AffineTransformRenderer
        ), "Renderer should be correct type"

    def test_model_bounds(self):
        """
        Test bounds calculation for a Model.
        """
        model = Model()
        model.add_poly(box(0, 0, 10, 10))
        model.add_poly(box(20, 20, 30, 30))
        assert model.minx == 0, "minx should be correct"
        assert model.miny == 0, "miny should be correct"
        assert model.maxx == 30, "maxx should be correct"
        assert model.maxy == 30, "maxy should be correct"

    def test_model_layers(self):
        """
        Test layer extraction from a Model.
        """
        model = Model()
        model.add_poly(box(0, 0, 10, 10), layer="layer1")
        model.add_poly(box(20, 20, 30, 30), layer="layer2")
        layers = model.layers
        assert "layer1" in layers, "Should contain 'layer1'"
        assert "layer2" in layers, "Should contain 'layer2'"

    def test_get_text_polygon(self):
        """
        Test generating a text polygon.
        """
        text = "A"
        poly = get_text_polygon(text)
        assert isinstance(
            poly, (Polygon, MultiPolygon)
        ), "Should return a Polygon or MultiPolygon"
        assert not poly.is_empty, "Polygon should not be empty"

    def test_affine_transform_renderer_translate(self):
        """
        Test AffineTransformRenderer with translation.
        """
        renderer = AffineTransformRenderer()
        renderer.translate(10, 20, 30)  # Apply translation
        poly = box(0, 0, 10, 10)  # Create a simple polygon
        transformed = renderer.transform(poly)  # Transform the polygon

        # Render to OpenSCAD string
        rendered_output = transformed._render()

        print(rendered_output)

        # Regex to check for the translate transformation
        match = re.search(
            r"translate\(\s?v\s?=\s?\[10,\s?20,\s?30\]\)", rendered_output
        )
        assert (
            match is not None
        ), "SCAD output should include the translate([10, 20, 30]) transformation"

    def test_affine_transform_renderer_color(self):
        """
        Test AffineTransformRenderer color transformation.
        """
        renderer = AffineTransformRenderer()
        renderer.color(1, 0, 0)  # Set color to red
        poly = box(0, 0, 10, 10)  # Create a simple polygon
        transformed = renderer.transform(poly)  # Transform the polygon

        # Render to OpenSCAD string
        rendered_output = transformed._render()

        # Check for the color part in the SCAD string using regex
        # The string we're looking for will look something like:
        # color(alpha = 1.0000000000, c = [1, 0, 0])
        match = re.search(r"color\(.*c\s?=\s?\[1,\s?0,\s?0\]\)", rendered_output)
        assert (
            match is not None
        ), "SCAD output should include the color transformation with c=[1, 0, 0]"
