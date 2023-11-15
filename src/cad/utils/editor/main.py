import time
from pathlib import Path

import dill
import ezdxf
import numpy as np
import trimesh
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (
    Callback,
    Color,
    Line,
    Mesh,
    PopMatrix,
    PushMatrix,
    RenderContext,
    Rotate,
    Scale,
    Translate,
    UpdateNormalMatrix,
)
from kivy.graphics.opengl import GL_DEPTH_TEST, glDisable, glEnable
from kivy.graphics.transformation import Matrix
from kivy.resources import resource_find
from kivy.support import install_twisted_reactor
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious, ActionView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon
from shapely.ops import unary_union
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from cad.utils.editor.data import EditorPacket, ExtrudedModel

# Ordering: this must come before twisted imports
install_twisted_reactor()

# Ordering: Twisted imports
from twisted.internet import protocol, reactor  # noqa: E402


class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find("simple.glsl")
        super(Renderer, self).__init__(**kwargs)
        self.mesh = None
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.0)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, delta):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas["projection_mat"] = proj
        modelview = Matrix().look_at(0, 0, 5, 0, 0, 0, 0, 1, 0)
        self.canvas["modelview_mat"] = modelview
        self.canvas["diffuse_light"] = (1.0, 1.0, 0.8)
        self.canvas["ambient_light"] = (0.1, 0.1, 0.1)
        self.rot.angle += delta * 100

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -10)
        UpdateNormalMatrix()
        self.rot = Rotate(1, 0, 1, 0)

        from shapely.geometry import box

        shape = box(0, 0, 10, 10) - box(2, 2, 8, 8)

        from shapely.affinity import scale

        mesh = trimesh.creation.extrude_polygon(shape, 5)

        self.set_geometry(mesh)

        PopMatrix()

    def set_geometry(self, mesh):
        if self.mesh:
            self.canvas.remove(self.mesh)

        UpdateNormalMatrix()

        # Vertices need to be a 1D array of the form:
        # [x1, y1, z1, xn1, yn1, zn1, x2, y2, z2, xn2, yn2, zn2, ...]
        # where x, y, z are the vertex coordinates and xn, yn, zn are the vertex normals

        vertices = np.concatenate(
            (mesh.vertices, mesh.vertex_normals), axis=1
        ).flatten()

        vertices = vertices.astype("float32")

        self.mesh = Mesh(
            vertices=vertices,
            indices=mesh.faces.flatten(),
            fmt=[(b"v_pos", 3, "float"), (b"v_normal", 3, "float")],
            mode="triangles",
        )
        self.canvas.add(self.mesh)


class Canvas2D(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry = None

        self.bind(size=self.update_canvas)
        self.bind(pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()

        if self.geometry is None:
            return

        # Get the bounds of the geometry
        bounds = self.geometry.bounds

        # Calculate the center of the bounds
        center_x = (bounds[0] + bounds[2]) / 2
        center_y = (bounds[1] + bounds[3]) / 2

        # Calculate the scale factor to fit the geometry in the viewport
        scale_factor = min(
            self.width / (bounds[2] - bounds[0]),
            self.height / (bounds[3] - bounds[1]),
        )

        with self.canvas:
            # Translate the canvas to center the geometry
            Translate(
                self.width / 2 - center_x * scale_factor,
                self.height / 2 - center_y * scale_factor,
                0,
            )

            # Scale the canvas to fit the geometry in the viewport
            Scale(scale_factor, scale_factor, 1)

            def render_polygon(polygon):
                Line(points=list(polygon.exterior.coords), width=1)
                for interior in polygon.interiors:
                    Line(points=list(interior.coords), width=1)

            Color(1, 1, 1, 1)
            if isinstance(self.geometry, MultiLineString):
                for line in self.geometry.geoms:
                    Line(points=list(line.coords), width=1)
            elif isinstance(self.geometry, Polygon):
                render_polygon(self.geometry)
            elif isinstance(self.geometry, MultiPolygon):
                for polygon in self.geometry.geoms:
                    render_polygon(polygon)

    def clear_shapes(self):
        self.geometry = None

    def set_geometry(self, geometry):
        self.geometry = geometry


class ObserverEventHandler(FileSystemEventHandler):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.path = None

    def on_modified(self, event):
        src_path = Path(event.src_path)
        if src_path == self.path:
            print("Reloading file")
            Clock.schedule_once(lambda dt: self.app.open_file(self.path), 0.2)


class EditorServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EditorServerFactory(protocol.Factory):
    protocol = EditorServer

    def __init__(self, app):
        self.app = app


class RendererApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Window.bind(on_drop_file=self.on_drop_file)
        self.popup = None
        self.observer = None
        self.observer_handler = ObserverEventHandler(self)

        reactor.listenTCP(17348, EditorServerFactory(self))

    def build(self):
        self.view_3d = Renderer()
        self.view_2d = Canvas2D()

        top_layout = BoxLayout(orientation="vertical")

        action_bar = ActionBar()
        av = ActionView()
        av.add_widget(ActionPrevious(title="Renderer", with_previous=False))
        av.add_widget(ActionButton(text="Open", on_release=self.show_open_file_dialog))
        action_bar.add_widget(av)

        top_layout.add_widget(action_bar)

        layout = GridLayout(cols=2)
        layout.add_widget(self.view_3d)
        layout.add_widget(self.view_2d)

        top_layout.add_widget(layout)

        return top_layout

    def show_open_file_dialog(self, instance):
        filechoose = FileChooserListView(path=Path(__file__).parent.as_posix())
        self.popup = Popup(title="Open File", content=filechoose, size_hint=(0.9, 0.9))
        filechoose.bind(on_submit=self.handle_open_file_select)
        self.popup.open()

    def handle_open_file_select(self, instance, selection, touch):
        if self.popup:
            self.popup.dismiss()

        path = Path(selection[0])

        if self.observer is not None:
            self.observer.stop()
            self.observer.join()

        self.observer = Observer()
        self.observer_handler.path = path
        self.observer.schedule(self.observer_handler, path.parent.as_posix())
        self.observer.start()

        self.open_file(path)

    def open_file(self, path):
        if path.suffix == ".dxf":
            self.handle_dxf_file(path)

    def handle_dxf_file(self, path):
        doc = ezdxf.readfile(path)

        msp = doc.modelspace()

        self.view_2d.clear_shapes()

        line_strings = []

        for e in msp:
            if e.dxftype() == "LINE":
                # line_strings.append(LineString([e.dxf.start, e.dxf.end]))
                pass
            elif e.dxftype() == "LWPOLYLINE":
                line_strings.append(LineString([[p[0], p[1]] for p in e.get_points()]))

        self.view_2d.set_geometry(unary_union(line_strings))

        self.view_2d.update_canvas()

    def on_drop_file(self, widget, filename, *args):
        filename = filename.decode("utf-8")
        self.handle_open_file_select(None, [filename], None)

    def handle_message(self, message):
        packet = dill.loads(message)

        if packet.key == "extruded_model":
            extruded_model: ExtrudedModel = packet.data
            self.view_2d.clear_shapes()

            self.view_2d.set_geometry(extruded_model.shape)

            self.view_2d.update_canvas()

            mesh = trimesh.creation.extrude_polygon(
                extruded_model.shape, extruded_model.thickness
            )

            self.view_3d.set_geometry(mesh)


if __name__ == "__main__":
    RendererApp().run()
