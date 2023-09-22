import numpy as np

from agile_ai.geometry.mesh_builder import MeshBuilder


class Sor(MeshBuilder):
    """Origin centered plane."""

    def __init__(self, heights, radii, n_thetas, endpoint=False, store_theta_phi=False):
        """Create the SoR."""
        MeshBuilder.__init__(self)
        thetas = np.linspace(0, np.pi * 2, n_thetas, endpoint=endpoint)
        self.store_theta_phi = store_theta_phi
        X = np.cos(thetas)
        Y = np.sin(thetas)
        X = np.append(X, X[0])
        Y = np.append(Y, Y[0])
        thetas = np.append(thetas, thetas[0])
        n_heights = len(heights)
        self.add_cross_section(X, Y, radii[0], heights[0],
                               thetas, reverse=True)
        self.add_cross_section(X, Y, radii[-1], heights[-1],
                               thetas, reverse=False)
        for h_i in range(n_heights - 1):
            h_b = heights[h_i]
            h_t = heights[h_i + 1]
            r_b = radii[h_i]
            r_t = radii[h_i + 1]
            phi_t = np.arcsin(h_t/np.sqrt(r_t**2+h_t**2))
            phi_b = np.arcsin(h_b/np.sqrt(r_b**2+h_b**2))
            for i in range(n_thetas):
                x_i = X[i]
                x_j = X[i + 1]
                y_i = Y[i]
                y_j = Y[i + 1]
                theta_i = thetas[i]
                theta_j = thetas[i + 1]
                Vit = (x_i * r_t, y_i * r_t, h_t, theta_i, phi_t)
                Vjt = (x_j * r_t, y_j * r_t, h_t, theta_j, phi_t)
                Vib = (x_i * r_b, y_i * r_b, h_b, theta_i, phi_b)
                Vjb = (x_j * r_b, y_j * r_b, h_b, theta_j, phi_b)
                Vs = (Vit, Vjt, Vjb, Vib)[::-1]
                if not store_theta_phi:
                    Vs = [vertex[:3] for vertex in Vs]
                self.add_quad_v(*Vs)
        if self.store_theta_phi:
            X, Y, Z, self.vertex_thetas, self.vertex_phis = np.array(self._v_list).T
            self._v_list = np.array((X, Y, Z)).T
        self.build()

    def add_cross_section(self, X, Y, r, h, thetas, reverse=False):
        """Add cross section."""
        phi = np.arcsin(h/np.sqrt(r**2+h**2))
        for i, theta_i in enumerate(thetas[:-1]):
            x_a = X[i] * r
            x_b = X[i + 1] * r
            y_a = Y[i] * r
            y_b = Y[i + 1] * r
            Va = (x_a, y_a, h, theta_i, phi)
            Vb = (x_b, y_b, h, theta_i, phi)
            Vc = (0, 0, h, theta_i, phi)
            if not self.store_theta_phi:
                Va, Vb, Vc = [vertex[:3] for vertex in [Va, Vb, Vc]]
            if reverse:
                self.add_tri_v(Vc, Vb, Va)
            else:
                self.add_tri_v(Va, Vb, Vc)


class Cylinder(Sor):
    """Create cylinder."""

    def __init__(self, n_heights=5, n_thetas=36):
        """Initialize SoR with unit cylinder."""
        heights = np.linspace(0, 1, n_heights)
        radii = np.ones_like(heights)
        Sor.__init__(self, heights, radii, n_thetas)


class Cone(Sor):
    """Create cone."""

    def __init__(self, n_heights=5, n_thetas=36):
        """Initialize SoR with unit cylinder."""
        heights = np.linspace(0, 1, n_heights)
        radii = np.linspace(1, 0, n_heights)
        Sor.__init__(self, heights, radii, n_thetas)


class Sphere(Sor):
    """Create sphere."""

    def __init__(self, n_heights=36, n_thetas=36, **kwargs):
        """Initialize SoR with unit sphere."""
        radii = np.sin(np.linspace(0, np.pi, n_heights)) / 2.0
        heights = np.cos(np.linspace(np.pi, 0, n_heights)) / 2.0 + .5
        Sor.__init__(self, heights, radii, n_thetas, **kwargs)


class Wine(Sor):
    """Create wine class."""

    def __init__(self, n_heights=100, n_thetas=36):
        """Create a wine class generatrix."""
        H = np.linspace(0, 15, n_heights)
        R = np.zeros_like(H)
        # For 0<x<1 (base)
        G = (H <= 1)
        R[G] = 3.5 - 2.5 * H[G] ** 2
        # For 1<x<7 (stem)
        G = (H > 1) * (H <= 7)
        R[G] = 1
        # For 7<x<15(cup)
        G = (H > 7) * (H <= 15)
        R[G] = 3.5 - (5 / 128.0) * (H[G] - 15) ** 2
        Sor.__init__(self, H / 15.0, R / 15.0, n_thetas)
