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
