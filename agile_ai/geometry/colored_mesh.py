import numpy as np

from agile_ai.geometry.mesh import Mesh


class ColoredMesh:
    mesh: Mesh
    def __init__(self, mesh: Mesh, triangle_color=None, triangle_colors=None):
        self.mesh = mesh
        self._triangle_color = triangle_color
        self._triangle_colors = triangle_colors

    def get_triangle_colors(self):
        if self._triangle_colors is None:
            triangle_colors = np.empty((self.mesh.face_count, 3), dtype=np.uint8)
            triangle_colors[:] = self._triangle_color
            return triangle_colors
        else:
            return self._triangle_colors

    def get_triangle_vertices(self):
        return self.mesh.get_triangle_vertices()