from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (
    Callback,
    Color,
    Mesh,
    PopMatrix,
    PushMatrix,
    RenderContext,
    Rotate,
    Translate,
    UpdateNormalMatrix,
)
from kivy.graphics.opengl import GL_DEPTH_TEST, glDisable, glEnable
from kivy.graphics.transformation import Matrix
from kivy.resources import resource_find
from kivy.support import install_twisted_reactor
from kivy.uix.widget import Widget

# Ordering: this must come before twisted imports
install_twisted_reactor()

# Ordering: Twisted imports
from twisted.internet import protocol, reactor  # noqa: E402


class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find("simple.glsl")
        super(Renderer, self).__init__(**kwargs)
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
        self.canvas["diffuse_light"] = (1.0, 1.0, 0.8)
        self.canvas["ambient_light"] = (0.1, 0.1, 0.1)
        self.rot.angle += delta * 100

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -3)
        self.rot = Rotate(1, 0, 1, 0)
        # m = list(self.scene.objects.values())[0]
        # UpdateNormalMatrix()
        # self.mesh = Mesh(
        #     vertices=m.vertices,
        #     indices=m.indices,
        #     fmt=m.vertex_format,
        #     mode="triangles",
        # )
        PopMatrix()


class RendererApp(App):
    def build(self):
        return Renderer()

    def handle_message(self, message):
        print(message)


if __name__ == "__main__":
    RendererApp().run()
