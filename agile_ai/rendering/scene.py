from dataclasses import dataclass
from typing import List, NamedTuple, Callable

import numpy as np

from agile_ai.geometry.colored_mesh import ColoredMesh
from agile_ai.injection.interfaces import Service


@dataclass
class MeshEntry:
    colored_mesh: ColoredMesh
    visible: bool = True

    def get_triangle_colors(self):
        return self.colored_mesh.get_triangle_colors()

    def get_triangle_vertices(self):
        return self.colored_mesh.get_triangle_vertices()


def noop(*args, **kwargs):
    pass


class SceneCallbacks(NamedTuple):
    clear_meshes_callback: Callable = noop
    add_mesh_callback: Callable = noop
    set_camera_geometry_callback: Callable = noop
    set_frame_camera_world_callback: Callable = noop


class Scene(Service):
    mesh_list: List[MeshEntry]
    callbacks: SceneCallbacks

    def __init__(self, callbacks=None):
        if callbacks is None:
            callbacks = SceneCallbacks()
        self.callbacks = callbacks
        self.mesh_list = []
        self.K = np.eye(3)
        self.F_camera_world = None
        self.width = None
        self.height = None

    def clear_meshes(self):
        self.mesh_list = []
        self.callbacks.clear_meshes_callback()

    def add_mesh(self, mesh):
        index = len(self.mesh_list)
        self.mesh_list.append(MeshEntry(mesh))
        self.callbacks.add_mesh_callback(mesh, index)
        return index

    def disable_mesh(self, index):
        self.mesh_list[index].visible = False

    def enable_mesh(self, index):
        self.mesh_list[index].visible = True

    def set_camera_geometry(self, fx, fy, cx, cy, w, h):
        self.K = np.eye(3)
        self.K[0, 0] = fx
        self.K[1, 1] = fy
        self.K[0, -1] = cx
        self.K[1, -1] = cy
        self.width = w
        self.height = h
        self.callbacks.set_camera_geometry_callback(fx, fy, cx, cy, w, h)

    def set_frame_camera_world(self, F_camera_world):
        self.F_camera_world = F_camera_world
        self.callbacks.set_frame_camera_world_callback(F_camera_world)

    def set_frame_world_camera(self, F_world_camera):
        F_camera_world = np.linalg.inv(F_world_camera)
        self.set_frame_camera_world(F_camera_world)

    def get_visible_mesh_entries(self) -> List[MeshEntry]:
        return [e for e in self.mesh_list if e.visible]

    def enumerate_visible_mesh_entries(self):
        return [(i, e) for (i, e) in enumerate(self.mesh_list) if e.visible]

    def set_callbacks(self, callbacks: SceneCallbacks):
        self.callbacks = callbacks
