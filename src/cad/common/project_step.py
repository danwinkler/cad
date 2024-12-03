"""
Project step allows recording snapshots of geometry, images, etc during the execution of a model script. 

This is mostly used for capturing intermediate steps such that they can then be added to a blog.
"""

from dataclasses import dataclass

import aggdraw
import cv2
import numpy as np
import pixie
import shapely.geometry
from PIL import Image


class Step:
    def __init__(self, obj, desc, key):
        self.obj = obj
        self.desc = desc
        self.key = key

    def render(self, path):
        raise NotImplementedError()


class ShapelyStep(Step):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._margin = 0

    def render(self, settings, path):
        # I'd like to use pixie here, but it seems to have some png export issues
        self._render_pil(settings, path)

    def _render_pixie(self, settings, path):
        """
        Pixie seems to have some png export issues
        """
        image = pixie.Image(
            settings.image_width,
            settings.image_height,
        )
        image.fill(pixie.Color(1, 1, 1, 1))

        ctx = image.new_context()

        obj_width = self.obj.bounds[2] - self.obj.bounds[0]
        obj_height = self.obj.bounds[3] - self.obj.bounds[1]

        obj_ratio = obj_width / obj_height
        image_draw_area_width = settings.image_width - 2 * self._margin
        image_draw_area_height = settings.image_height - 2 * self._margin
        image_draw_area_ratio = image_draw_area_width / image_draw_area_height

        # Calculate the scaling ratio based on the smaller dimension
        scaling_ratio = min(
            image_draw_area_width / obj_width, image_draw_area_height / obj_height
        )

        # Calculate the offsets to center the object within the image draw area
        x_offset = (
            self._margin + (image_draw_area_width - (obj_width * scaling_ratio)) / 2
        )
        y_offset = (
            self._margin + (image_draw_area_height - (obj_height * scaling_ratio)) / 2
        )

        def to_image_space(p):
            # Calculate the scaled coordinates
            x = (p[0] - self.obj.bounds[0]) * scaling_ratio
            y = (p[1] - self.obj.bounds[1]) * scaling_ratio

            x += x_offset
            y += y_offset

            return x, y

        if isinstance(self.obj, shapely.geometry.LineString):
            for i in range(len(self.obj.coords) - 1):
                ax, ay = to_image_space(self.obj.coords[i])
                bx, by = to_image_space(self.obj.coords[i + 1])
                ctx.stroke_segment(ax, ay, bx, by)
        elif isinstance(
            self.obj, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)
        ):
            geoms = (
                [self.obj]
                if isinstance(self.obj, shapely.geometry.Polygon)
                else self.obj.geoms
            )
            for geom in geoms:
                for ring in geom.interiors:
                    for i in range(len(ring.coords) - 1):
                        ax, ay = to_image_space(ring.coords[i])
                        bx, by = to_image_space(ring.coords[i + 1])
                        ctx.stroke_segment(ax, ay, bx, by)
                for i in range(len(geom.exterior.coords) - 1):
                    ax, ay = to_image_space(geom.exterior.coords[i])
                    bx, by = to_image_space(geom.exterior.coords[i + 1])
                    ctx.stroke_segment(ax, ay, bx, by)

        image.write_file(str(path))

    def _render_pil(self, settings, path):
        image = Image.new(
            "RGB", (settings.image_width, settings.image_height), (255, 255, 255)
        )
        draw = aggdraw.Draw(image)
        pen = aggdraw.Pen((0, 0, 0), 1)

        obj_width = self.obj.bounds[2] - self.obj.bounds[0]
        obj_height = self.obj.bounds[3] - self.obj.bounds[1]

        obj_ratio = obj_width / obj_height
        image_draw_area_width = settings.image_width - 2 * self._margin
        image_draw_area_height = settings.image_height - 2 * self._margin
        image_draw_area_ratio = image_draw_area_width / image_draw_area_height

        # Calculate the scaling ratio based on the smaller dimension
        scaling_ratio = min(
            image_draw_area_width / obj_width, image_draw_area_height / obj_height
        )

        # Calculate the offsets to center the object within the image draw area
        x_offset = (
            self._margin + (image_draw_area_width - (obj_width * scaling_ratio)) / 2
        )
        y_offset = (
            self._margin + (image_draw_area_height - (obj_height * scaling_ratio)) / 2
        )

        def to_image_space(p):
            # Calculate the scaled coordinates
            x = (p[0] - self.obj.bounds[0]) * scaling_ratio
            y = (p[1] - self.obj.bounds[1]) * scaling_ratio

            x += x_offset
            y += y_offset

            return x, y

        if isinstance(self.obj, shapely.geometry.LineString):
            for i in range(len(self.obj.coords) - 1):
                ax, ay = to_image_space(self.obj.coords[i])
                bx, by = to_image_space(self.obj.coords[i + 1])
                draw.line((ax, ay, bx, by), pen)
        elif isinstance(
            self.obj, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)
        ):
            geoms = (
                [self.obj]
                if isinstance(self.obj, shapely.geometry.Polygon)
                else self.obj.geoms
            )
            for geom in geoms:
                for ring in geom.interiors:
                    for i in range(len(ring.coords) - 1):
                        ax, ay = to_image_space(ring.coords[i])
                        bx, by = to_image_space(ring.coords[i + 1])
                        draw.line((ax, ay, bx, by), pen)
                for i in range(len(geom.exterior.coords) - 1):
                    ax, ay = to_image_space(geom.exterior.coords[i])
                    bx, by = to_image_space(geom.exterior.coords[i + 1])
                    draw.line((ax, ay, bx, by), pen)

        draw.flush()
        image.save(path)

    def margin(self, margin):
        self._margin = margin

    @staticmethod
    def can_render(obj):
        return isinstance(
            obj,
            (
                shapely.geometry.LineString,
                shapely.geometry.Polygon,
                shapely.geometry.MultiPolygon,
            ),
        )


class ImageStep(Step):
    def render(self, settings, path):
        if isinstance(self.obj, np.ndarray):
            im = self.obj

            if im.dtype == np.uint16:
                im = cv2.convertScaleAbs(im)

            im = cv2.resize(im, (settings.image_width, settings.image_height))

            cv2.imwrite(str(path), im)

    def can_render(obj):
        return isinstance(obj, (np.ndarray, Image))


@dataclass
class ProjectStepSettings:
    image_width: int = 512
    image_height: int = 512


class ProjectSteps:
    STEP_CLASSES = [ShapelyStep, ImageStep]

    def __init__(self, settings=ProjectStepSettings()):
        self.steps = []
        self.added = set()
        self.settings = settings

    def record(self, obj, desc=None, key=None):
        for step_class in self.STEP_CLASSES:
            if step_class.can_render(obj):
                step_obj = step_class(obj, desc, key)

                if not (key and key in self.added):
                    self.steps.append(step_obj)

                if key:
                    self.added.add(key)

                return step_obj

    def render(self, path):
        if not path.exists():
            path.mkdir(parents=True)

        gitignore = path / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("*.png")

        for i, step in enumerate(self.steps):
            key = step.key or i
            step_path = path / f"{key}.png"
            print(f"Rendering {step_path}")
            step.render(settings=self.settings, path=step_path)
