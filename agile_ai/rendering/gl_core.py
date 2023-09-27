from collections import namedtuple

import numpy as np

Rx180 = np.eye(4)
Rx180[1, 1] = -1
Rx180[2, 2] = -1


class GLCore:
    F_opengl_camera = Rx180
    RenderedImages = namedtuple("RenderedImages", "color depth xyz_camera xyz_world")

    def __init__(self):
        self.framebuffer = None
        self.width = None
        self.height = None
        self.buffer_width = None
        self.buffer_height = None
        self.buffer_size = None
        self.z_near = None
        self.z_far = None
        self.window_handle = None
        self.initialized = False

    def configure(self, z_near, z_far):
        self.z_near = z_near
        self.z_far = z_far

    def set_buffer_size(self, buffer_width, buffer_height):
        self.buffer_width = buffer_width
        self.buffer_height = buffer_height
        self.buffer_size = (buffer_width, buffer_height)

    def set_frame_camera_world(self, F_camera_world):
        F_opengl_world = self.F_opengl_camera @ F_camera_world
        self.set_frame_opengl_world(F_opengl_world)

    def set_frame_opengl_world(self, F_opengl_world):
        self.set_modelview_matrix(F_opengl_world)

    def initialize(self, buffer_width: int, buffer_height: int):
        raise NotImplementedError

    def set_modelview_matrix(self, F_camera_world):
        raise NotImplementedError

    def get_frame_opengl_world(self):
        raise NotImplementedError

    def get_projection_matrix(self):
        raise NotImplementedError

    def get_modelview_matrix(self):
        raise NotImplementedError

    def get_frame_world_opengl(self):
        F_opengl_world = self.get_frame_opengl_world()
        F_world_opengl = np.linalg.inv(F_opengl_world)
        return F_world_opengl

    def add_mesh(self, mesh, index):
        raise NotImplementedError

    def clear_meshes(self):
        raise NotImplementedError

    def render_indices(self, indices):
        raise NotImplementedError

    def set_frustum(self, l, r, t, b, z_near, z_far):
        raise NotImplementedError

    def set_camera_size(self, width, height):
        self.width = width
        self.height = height

    def set_camera_perspective(self, cam_params):
        fx, fy, cx, cy, w, h = cam_params
        z_near, z_far = self.z_near, self.z_far
        self.set_camera_size(w, h)
        # Flip up-down
        cy = h - cy

        l = -z_near * cx / fx
        r = z_near * (w - cx) / fx
        b = -z_near * cy / fy
        t = z_near * (h - cy) / fy

        self.set_frustum(l, r, t, b, z_near, z_far)
