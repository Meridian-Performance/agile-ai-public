from typing import NamedTuple

import cv2
import numpy as np

from agile_ai.injection.interfaces import Service
from agile_ai.rendering.renderer_interface import RendererInterface
from agile_ai.rendering.scene import Scene, SceneCallbacks


class RenderData(NamedTuple):
    color: np.ndarray


class CvRenderer(RendererInterface, Service):
    scene: Scene

    def __init__(self):
        callbacks = SceneCallbacks(set_camera_geometry_callback=self._set_camera_geometry)
        self.scene = Scene(callbacks)
        self.color_image = None

    def clear_color(self):
        self.color_image[:] = 0

    def _set_camera_geometry(self, fx, fy, cx, cy, w, h):
        self.color_image = np.zeros((h, w, 3), dtype=np.uint8)

    def render_3d_triangle(self, vertices, color=None):
        if color is None:
            color = (255, 255, 255)
        R_camera_world = self.scene.F_camera_world[:3, :3]
        t_camera_world = self.scene.F_camera_world[:3, -1][None].T
        X_world_vertices = vertices.T
        X_camera_vertices = (R_camera_world @ X_world_vertices) + t_camera_world
        X_image_vertices = (self.scene.K @ X_camera_vertices)
        vertices = (X_image_vertices[:2] / X_image_vertices[-1]).T
        self.render_2d_triangle(vertices, color)

    def render_2d_triangle(self, vertices, color=None):
        if color is None:
            color = (255, 255, 255)
        else:
            color = tuple([int(c) for c in color])
        pts = vertices.astype(np.int32)
        cv2.fillPoly(self.color_image, [pts], color)  # noqa

    def render(self):
        for mesh_entry in self.scene.get_visible_mesh_entries():
            for vertices, color in zip(mesh_entry.get_triangle_vertices(), mesh_entry.get_triangle_colors()):
                self.render_3d_triangle(vertices, color=color)

    def get_data(self, color=True, depth=False):
        return RenderData(self.color_image)
