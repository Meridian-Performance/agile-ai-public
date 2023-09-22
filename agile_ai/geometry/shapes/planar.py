import numpy as np

from agile_ai.geometry.mesh_builder import MeshBuilder


class Plane(MeshBuilder):
    """Origin centered plane."""

    def __init__(self):
        """Create the plane."""
        MeshBuilder.__init__(self)
        X = [+1, +1, -1, -1][::-1]
        Y = [+1, -1, -1, +1][::-1]
        Z = [0, 0, 0, 0]
        Vs = list(zip(X, Y, Z))
        self.add_quad_v(*Vs)
        self.build()

    @staticmethod
    def get_test_planes():
        # Create planes in the camera coordinate system that
        # show 4 planes in the u,v image as: 
        # [R][B]
        # [G][Y]
        #
        # Create 1x1 plane (0, 0, 1) --- (1, 1, 1)
        plane = Plane()
        plane.translate((1, 1, 2))
        plane.scale(.5)
        # plane_y (0, 0, 1) --- (1, 1, 1)
        plane_y = plane.copy()
        plane_y.get_triangle_colors = lambda: np.array([(255, 255, 0)] * 2, dtype=np.uint8)
        # plane_g (-1, 0, 1) --- (0, 1, 1)
        plane_g = plane.copy()
        plane_g.translate((-1, 0, 0))
        plane_g.get_triangle_colors = lambda: np.array([(0, 255, 0)] * 2, dtype=np.uint8)
        # plane_r (-1, -1, 1) --- (0, 0, 1)
        plane_r = plane.copy()
        plane_r.translate((-1, -1, 0))
        plane_r.get_triangle_colors = lambda: np.array([(255, 0, 0)] * 2, dtype=np.uint8)
        # plane_b (0, -1, 1) --- (1, 0, 1)
        plane_b = plane.copy()
        plane_b.translate((0, -1, 0))
        plane_b.get_triangle_colors = lambda: np.array([(0, 0, 255)] * 2, dtype=np.uint8)
        return [plane_r, plane_g, plane_b, plane_y]


class Circle(MeshBuilder):
    """Origin centered circle."""

    def __init__(self, n=36):
        """Create the plane."""
        MeshBuilder.__init__(self)
        thetas = np.linspace(0, np.pi * 2, n)
        X = np.cos(thetas)
        Y = np.sin(thetas)
        X[-1] = X[0]
        Y[-1] = Y[0]
        X = np.append(X, X[0])
        Y = np.append(Y, Y[0])
        Vc = (0, 0, 0)
        self.add_vertex(Vc)
        for i in range(n):
            x_a = X[i]
            x_b = X[i + 1]
            y_a = Y[i]
            y_b = Y[i + 1]
            Va = (x_a, y_a, 0)
            Vb = (x_b, y_b, 0)
            self.add_tri_v(Va, Vb, Vc)
        self.build()
