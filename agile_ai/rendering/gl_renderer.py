from .renderer_interface import RendererInterface
from .scene import Scene, SceneCallbacks
from .gl_core import GLCore


class GLRenderer(RendererInterface):
    min_buffer_size = None
    core: GLCore
    scene: Scene

    @classmethod
    def set_min_buffer_size(cls, buffer_width, buffer_height):
        cls.min_buffer_size = (buffer_width, buffer_height)

    def initialize_core(self, buffer_width, buffer_height, z_near=0.01, z_far=100.0):
        if self.min_buffer_size:
            buffer_width = max(buffer_width, self.min_buffer_size[0])
            buffer_height = max(buffer_height, self.min_buffer_size[1])
        print("Initializing core %s" % [buffer_width, buffer_height])
        self.core.configure(z_near, z_far)
        self.core.initialize(buffer_width, buffer_height)
        actual_size = self.core.buffer_size
        requested_size = (buffer_width, buffer_height)
        if actual_size < requested_size:
            raise ValueError("GLCore previously initialized with smaller "
                             "buffer than required %r vs %r." % (actual_size, requested_size))
        callbacks = SceneCallbacks(clear_meshes_callback=self.core.clear_meshes,
                                   add_mesh_callback=self.core.add_mesh,
                                   set_camera_geometry_callback=self._set_camera_geometry,
                                   set_frame_camera_world_callback=self.core.set_frame_camera_world
                                   )
        self.scene.set_callbacks(callbacks)

    def __init__(self):
        self.scene = Scene()
        self.color_image = None

    def _set_camera_geometry(self, fx, fy, cx, cy, w, h):
        self.initialize_core(w, h)
        self.core.set_camera_perspective((fx, fy, cx, cy, w, h))

    def render(self):
        indices = []
        for index, mesh_entry in self.scene.enumerate_visible_mesh_entries():
            indices.append(index)
        self.core.render_indices(indices)

    def get_data(self, color=True, depth=False, xyz_camera=False, xyz_world=False):
        return self.core.data(color=color, depth=depth,
                              xyz_camera=xyz_camera, xyz_world=xyz_world)
