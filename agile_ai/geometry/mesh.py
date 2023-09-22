"""Mesh representation."""
from typing import Iterable, Tuple

import numpy as np

from agile_ai.data_marshalling.numeric_types import FloatN3
from agile_ai.geometry.bounding_box import BoundingBox
from agile_ai.geometry.pose_conversions import similarity_to_rotation_translation_scale, Rx, Ry, Rz, Raxis


class MeshTransforms:
    vertices: FloatN3
    def get_bounding_box(self) -> BoundingBox:
        X, Y, Z = self.vertices.T
        x_min = X.min()
        x_max = X.max()
        y_min = Y.min()
        y_max = Y.max()
        z_min = Z.min()
        z_max = Z.max()
        return BoundingBox(x_min, x_max, y_min, y_max, z_min, z_max)

    def scale(self, scale):
        """Scale points."""
        if np.isscalar(scale):
            sx, sy, sz = scale, scale, scale
        else:
            sx, sy, sz = scale
        X, Y, Z = self.vertices.T
        X *= sx
        Y *= sy
        Z *= sz
        return self

    def translate(self, translation):
        """Scale points."""
        tx, ty, tz = translation
        X, Y, Z = self.vertices.T
        X += tx
        Y += ty
        Z += tz
        return self

    def center_midpoint(self):
        """Translate such that the midpoints are at (0, 0, 0)."""
        self.translate(-self.get_bounding_box().mid_point)
        return self

    def translate_to_xy_plane(self):
        """Translate such that the min_z point is at 0."""
        z_min = self.get_bounding_box().z_min
        self.translate((0, 0, -z_min))
        return self

    def rotate(self, R):
        """Rotates by R."""
        rx, ry, rz = R
        X, Y, Z = self.vertices.T
        Xrot = rx[0] * X + rx[1] * Y + rx[2] * Z
        Yrot = ry[0] * X + ry[1] * Y + ry[2] * Z
        Zrot = rz[0] * X + rz[1] * Y + rz[2] * Z
        X[:] = Xrot
        Y[:] = Yrot
        Z[:] = Zrot

    def transform(self, R: np.array = None, t: np.array = None, s: float = None, transform=None) -> None:
        """Apply transform or rotate by R, translate by t, scale by s."""
        X, Y, Z = self.vertices.T
        if transform is not None:
            R, t, s = similarity_to_rotation_translation_scale(transform)
        rx, ry, rz = R
        tx, ty, tz = t
        Xt = rx[0] * X + rx[1] * Y + rx[2] * Z + tx
        Yt = ry[0] * X + ry[1] * Y + ry[2] * Z + ty
        Zt = rz[0] * X + rz[1] * Y + rz[2] * Z + tz
        if s is not None:
            Xt *= s
            Yt *= s
            Zt *= s
        X[:] = Xt
        Y[:] = Yt
        Z[:] = Zt
        return self

    def rotate_x(self, theta):
        """Rotate around x by theta."""
        self.rotate(Rx(theta))
        return self

    def rotate_y(self, theta):
        """Rotate around x by theta."""
        self.rotate(Ry(theta))
        return self

    def rotate_z(self, theta):
        """Rotate around x by theta."""
        self.rotate(Rz(theta))
        return self

    def rotate_axis(self, axis, theta):
        """Rotate around axis by theta."""
        self.rotate(Raxis(axis, theta))
        return self


class Mesh(MeshTransforms):
    """Mesh representation."""
    mesh_names: Iterable[str]

    @property
    def face_count(self):
        return len(self.Fi)

    @property
    def vertex_count(self):
        return len(self.point_cloud)

    @staticmethod
    def from_mesh_list(mesh_list, merge_meshes=True):
        pass

    def __init__(self, vertices, faces,
                 mesh_names=None,
                 mesh_face_slice_indices=None,
                 mesh_vertex_slice_indices=None):
        self.faces = faces
        self.vertices = vertices
        if mesh_names is None:
            mesh_names = []
        if mesh_face_slice_indices is None:
            mesh_face_slice_indices = np.array([0, len(faces)], dtype=np.uint64)
        if mesh_vertex_slice_indices is None:
            mesh_vertex_slice_indices = np.array([0, len(vertices)], dtype=np.uint64)
        self.mesh_names = mesh_names
        self.mesh_face_slice_indices = mesh_face_slice_indices
        self.mesh_vertex_slice_indices = mesh_vertex_slice_indices

    def copy(self, dtype=None):
        pass

    def __eq__(self, other):
        """Test for equivalence."""
        return False

    def __add__(self, other: "Mesh"):
        """Add two meshes together"""

    @property
    def face_count(self):
        """Return the number of faces."""
        return len(self.faces)

    @property
    def face_normals(self):
        """Return face normals."""
        A, B, C = self.get_triangle_vertices()
        U = B - A
        V = C - A
        N = np.cross(U, V, axis=1)
        N /= np.linalg.norm(N, axis=1)[:, None]
        return N

    @property
    def face_centers(self):
        """Return face normals."""
        A, B, C = self.get_triangle_vertices()
        return (A + B + C) / 3.0

    @property
    def triangles(self):
        """Return triangles."""
        return self.vertices[self.faces]

    def get_triangle_vertices(self) -> Tuple:
        pass

    def get_triangle_color(self):
        return None

    def get_triangle_colors(self):
        raise NotImplementedError

    def set_triangle_colors(self, triangle_colors):
        pass

    def set_triangle_color(self, triangle_color):
        pass

    @staticmethod
    def compute_triangle_areas(triangle_vertices):
        """Compute triangle areas."""
        Va, Vb, Vc = triangle_vertices
        Vab = Va - Vb
        Vac = Va - Vc
        return np.abs(np.linalg.norm(np.cross(Vab, Vac), axis=1) / 2)

    @property
    def triangle_areas(self):
        """Return triangle areas."""
        return self.compute_triangle_areas(self.triangle_vertices)

    def get_sub_mesh_by_slice(self, face_slice, filter_vertices=True):
        pass

    def get_sub_mesh_by_index(self, index, filter_vertices=True) -> "Mesh":
        """Return a face group submesh."""
        pass

    def set_name(self, name: str):
        self.mesh_names = [name]
        self.mesh_face_slice_indices = np.array([0, len(self.Fi)], dtype=np.uint64)

    def with_name(self, name: str):
        self.set_name(name)
        return self