from pathlib import Path

import numpy as np
import pytest
from PIL import Image
from shapely.geometry import LineString, MultiPolygon, Polygon

from cad.common.project_step import ProjectSteps, ProjectStepSettings


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Temporary directory for output files during testing.
    """
    return tmp_path / "output"


@pytest.fixture
def project_steps():
    """
    Fixture for a ProjectSteps instance with default settings.
    """
    settings = ProjectStepSettings(image_width=256, image_height=256)
    return ProjectSteps(settings=settings)


@pytest.mark.llmgenerated
def test_record_shapely_step(project_steps):
    """
    Test recording a Shapely geometry step.
    """
    line = LineString([(0, 0), (10, 10), (20, 0)])
    step = project_steps.record(line, desc="Test Line", key="test_line")

    assert step is not None, "ShapelyStep should be created"
    assert len(project_steps.steps) == 1, "Step should be recorded"
    assert project_steps.steps[0].key == "test_line", "Step key should match"


@pytest.mark.llmgenerated
def test_record_image_step(project_steps):
    """
    Test recording an image step.
    """
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    step = project_steps.record(image, desc="Test Image", key="test_image")

    assert step is not None, "ImageStep should be created"
    assert len(project_steps.steps) == 1, "Step should be recorded"
    assert project_steps.steps[0].key == "test_image", "Step key should match"


@pytest.mark.llmgenerated
def test_render_steps(project_steps, temp_output_dir):
    """
    Test rendering recorded steps to disk.
    """
    # Record a LineString
    line = LineString([(0, 0), (10, 10), (20, 0)])
    project_steps.record(line, desc="Test Line", key="test_line")

    # Record a Polygon
    polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    project_steps.record(polygon, desc="Test Polygon", key="test_polygon")

    # Record an Image
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    project_steps.record(image, desc="Test Image", key="test_image")

    # Render all steps
    project_steps.render(temp_output_dir)

    # Assert output files are created
    step_files = list(temp_output_dir.glob("*.png"))
    assert len(step_files) == 3, "All steps should be rendered"
    assert (temp_output_dir / "test_line.png").exists(), "Line step should be rendered"
    assert (
        temp_output_dir / "test_polygon.png"
    ).exists(), "Polygon step should be rendered"
    assert (
        temp_output_dir / "test_image.png"
    ).exists(), "Image step should be rendered"


@pytest.mark.llmgenerated
def test_prevent_duplicate_keys(project_steps):
    """
    Test that duplicate keys are not recorded twice.
    """
    line = LineString([(0, 0), (10, 10), (20, 0)])
    project_steps.record(line, desc="Test Line", key="duplicate_key")
    project_steps.record(line, desc="Duplicate Line", key="duplicate_key")

    assert len(project_steps.steps) == 1, "Duplicate key should not be recorded twice"


@pytest.mark.llmgenerated
def test_render_gitignore(temp_output_dir, project_steps):
    """
    Test that a .gitignore file is created during rendering.
    """
    # Record a LineString
    line = LineString([(0, 0), (10, 10), (20, 0)])
    project_steps.record(line, desc="Test Line", key="test_line")

    # Render all steps
    project_steps.render(temp_output_dir)

    # Assert .gitignore is created
    gitignore_path = temp_output_dir / ".gitignore"
    assert gitignore_path.exists(), ".gitignore should be created"
    assert "*.png" in gitignore_path.read_text(), "Gitignore should include *.png"


@pytest.mark.llmgenerated
def test_render_polygon_with_holes(project_steps, temp_output_dir):
    """
    Test rendering a polygon with holes.
    """
    outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
    inner = [(3, 3), (7, 3), (7, 7), (3, 7)]
    polygon_with_hole = Polygon(outer, [inner])

    project_steps.record(polygon_with_hole, desc="Polygon with Hole", key="hole_test")

    # Render
    project_steps.render(temp_output_dir)

    # Assert output file is created
    output_path = temp_output_dir / "hole_test.png"
    assert output_path.exists(), "Polygon with holes should be rendered"


@pytest.mark.llmgenerated
def test_render_multipolygon(project_steps, temp_output_dir):
    """
    Test rendering a MultiPolygon.
    """
    poly1 = Polygon([(0, 0), (5, 0), (5, 5), (0, 5)])
    poly2 = Polygon([(10, 10), (15, 10), (15, 15), (10, 15)])
    multipolygon = MultiPolygon([poly1, poly2])

    project_steps.record(multipolygon, desc="MultiPolygon", key="multipolygon_test")

    # Render
    project_steps.render(temp_output_dir)

    # Assert output file is created
    output_path = temp_output_dir / "multipolygon_test.png"
    assert output_path.exists(), "MultiPolygon should be rendered"
