import numpy as np

from agile_ai.geometry.mesh import Mesh


class MeshBuilder(Mesh):
    """Class to build a mesh incrementally."""
    # pylint: disable=super-init-not-called
    def __init__(self):
        """Create builder data structures."""
        self._f_list = []
        self._v_list = []
        self._i_of_v = dict()

    def add_vertex(self, v):
        """Add a vertex if its not in the v_list, return its index."""
        v = tuple(v)
        if v in self._i_of_v:
            return self._i_of_v[v]
        i = len(self._v_list)
        self._i_of_v[v] = i
        self._v_list.append(v)
        return i

    def add_quad_v(self, va, vb, vc, vd):
        """Add a quad by vertex."""
        a = self.add_vertex(va)
        b = self.add_vertex(vb)
        c = self.add_vertex(vc)
        d = self.add_vertex(vd)
        self.add_quad(a, b, c, d)

    def add_tri_v(self, va, vb, vc):
        """Add a triangle by vertex."""
        a = self.add_vertex(va)
        b = self.add_vertex(vb)
        c = self.add_vertex(vc)
        self.add_tri(a, b, c)

    def add_quad(self, a, b, c, d):
        """Add a quad by vertex indices."""
        self.add_tri(a, b, c)
        self.add_tri(a, c, d)

    def add_tri(self, a, b, c):
        """Add a triangle by vertex indices."""
        self._f_list.append((a, b, c))

    def build(self):
        """Create the mesh."""
        vertices = np.array(self._v_list, dtype=np.float32)
        faces = np.array(self._f_list, dtype=np.uint32)
        Mesh.__init__(self,
                      vertices,
                      faces,
                      mesh_names=["mesh"],
                      mesh_vertex_slice_indices=np.array([0, len(vertices)]),
                      mesh_face_slice_indices=np.array([0, len(faces)])
                      )
        del self._f_list
        del self._v_list
        del self._i_of_v
