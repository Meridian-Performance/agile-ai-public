from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt

from agile_ai.data_marshalling.numeric_types import FloatN, BoolN
from agile_ai.estimation.svm.embedded_svm_estimator import EmbeddedSvmEstimator


class CircleSvmEstimator(EmbeddedSvmEstimator):
    def embed_exemplars(self, x_c, y_c):
        """
            Remaps point to a cone centered at (0, 0), where H = R
        """
        X = self.exemplars_2D.X
        Pz = np.linalg.norm(X - (x_c, y_c), axis=1)
        Px, Py = X.T
        Xnd = np.array((Px, Py, Pz)).T
        self.embedding_parameters = (x_c, y_c)
        self.exemplars_ND = self.exemplars_2D.with_points(Xnd)

    def reembed_exemplars(self):
        self.embed_exemplars(*self.new_embedding_parameters)

    def solve_conic(self):
        x_c, y_c = self.embedding_parameters
        """
            Cone:
                X, Y
                Z_cone = sqrt((X-x_c)**2 + (Y-x_c)**2)
                Z_cone**2 = (X-x_c)**2 + (Y-x_c)**2
                Z_cone**2 = X**2 + x_c**2 - 2(X)(x_c) + Y**2 + y_c**2 - 2(Y)(y_c)
                Z_cone**2 = (X**2 + Y**2) + - 2(X)(x_c) - 2(Y)(y_c) + (x_c**2 + y_c**2)
            Plane specified by (n, d)
                Z_plane = (a * X + b * Y + d) / -c = n_x * X + n_y * Y + w
                where a, b, c  = n, n_x = -a/c, n_y = -b/c, w = -d/c
            Conic section, assuming ellipse
                Z_cone = Z_plane
                Z_cone = n_x * X + n_y * Y + w
                Z_cone_sq = (n_x * X + n_y * Y + w)**2
                Z_cone_sq = (n_x * X + n_y * Y)**2 + 2(n_x * X + n_y * Y)w + w**2
                Z_cone_sq = (n_x * X + n_y * Y)**2 + 2(n_x)(w) * X + 2(n_y)(w) * Y + w**2
                Z_cone_sq = (n_x * X + n_y * Y)**2 + t_x * X + t_y * Y + w**2, t_x = 2(n_x)(w), t_y = 2(n_y)(w)
                Z_cone_sq = (n_x**2)(X**2) + (n_y**2)(Y**2) + 2(n_x)(n_y)(X)(Y) + t_x * X + t_y * Y + w**2
                Z_cone_sq = (n_x**2)(X**2) + (n_y**2)(Y**2) + t_xy(X)(Y) + t_x(X) + t_y(Y) + w**2, t_xy = 2(n_x)(n_y)
                Z_cone_sq = (n_x**2)(X**2) + (n_y**2)(Y**2) + t_xy(X)(Y) +    t_x(X) +    t_y(Y) + w**2
                Z_cone_sq =      (1)(X**2) +      (1)(Y**2) +          0 - 2(x_c)(X) - 2(y_c)(Y) + (x_c**2 + y_c**2)
            The canonical conic section:
                Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0
                A = (n_x**2-1)
                B = 2(n_x)(n_y)
                C = (n_y**2-1)
                D = 2(n_x)(w) + 2(x_c)
                E = 2(n_y)(w) + 2(y_c)
                F = w**2 - (x_c **2 + y_c**2)
        """
        w = self.intercept[0] / -self.normal[-1]
        n_x, n_y = self.normal[:2] / -self.normal[-1]
        A = n_x ** 2 - 1
        B = 2*n_x*n_y
        C = n_y ** 2 - 1
        D = 2*n_x*w + 2 * x_c
        E = 2*n_y*w + 2 * y_c
        F = w ** 2 - (x_c**2 + y_c**2)
        return A, B, C, D, E, F

    def compute_parameters(self):
        x_c, y_c = self.embedding_parameters
        self.conic_parameters = self.solve_conic()
        C = self.get_conic_matrix()
        x_c_new, y_c_new = np.linalg.inv(C[:2, :2]) @ -C[:2, -1]
        self.new_embedding_parameters = (x_c_new, y_c_new)
        U, s, Vt = np.linalg.svd(C[:2, :2])
        l = s ** 2
        # (X - x_c)**2 + (Y - y_c)**2 = r**2
        # X**2 + Y**2 - 2(X)(x_c) - 2(Y)(y_c) + x_c**2 + y_c**2 - r**2 = 0
        # A      C      D           E          F
        k = - np.linalg.det(C) / np.linalg.det(C[:2, :2])
        r = np.sqrt(np.mean(abs(k/l)))
        self.circle_parameters = np.array([1.0, 0.0, 1.0, -2.0*x_c_new, -2.0*y_c_new, x_c_new**2 + y_c_new**2 - r**2])

    def solve_quadratic(self, A: FloatN, B: FloatN, C: FloatN) -> Tuple[FloatN, FloatN, BoolN]:
        sqrt_discriminant = np.sqrt(B * B - 4 * A * C)
        denom = 2 * A
        Xn = (-B - sqrt_discriminant) / denom
        Xp = (-B + sqrt_discriminant) / denom
        return Xn, Xp, ~np.isnan(sqrt_discriminant)

    def rasterize_conic(self, num, conic_parameters, cone_parameters=None):
        L = np.linspace(-1, 2, num)
        # A * X**2 + B * X * Y + C * Y**2 + D * X + E * Y + F = 0
        A, B, C, D, E, F = conic_parameters
        Xl = L
        Cy = (A * Xl**2 + D * Xl + F)
        By = (B * Xl + E)
        Ay = C

        Yl = L
        Cx = (C * Yl**2 + E * Yl + F)
        Bx = (B * Yl + D)
        Ax = A

        Yn, Yp, My = self.solve_quadratic(Ay, By, Cy)
        Xn, Xp, Mx = self.solve_quadratic(Ax, Bx, Cx)

        X = [Xl[My], Xl[My], Xn[Mx], Xp[Mx]]
        Y = [Yn[My], Yp[My], Yl[Mx], Yl[Mx]]
        if cone_parameters:
            x_c, y_c = cone_parameters
            Zyn = np.sqrt((Xl-x_c)**2 + (Yn-y_c)**2)
            Zyp = np.sqrt((Xl-x_c)**2 + (Yp-y_c)**2)
            Zxn = np.sqrt((Xn-x_c)**2 + (Yl-y_c)**2)
            Zxp = np.sqrt((Xp-x_c)**2 + (Yl-y_c)**2)
            Z = [Zyn[My], Zyp[My], Zxn[Mx], Zxp[Mx]]
            P = [np.array([x, y, z]).T for (x, y, z) in zip(X, Y, Z)]
        else:
            P = [np.array([x, y]).T for (x, y) in zip(X, Y)]
        return P

    def get_conic_matrix(self):
        conic_parameters = self.conic_parameters
        A, B, C, D, E, F = conic_parameters
        return np.array([(A, B/2, D/2), (B/2, C, E/2), (D/2, E/2, F)])

    def visualize_decision_surface_ND(self):
        cone_parameters = self.embedding_parameters
        conic_parameters = self.conic_parameters
        ax = self.visualize_predictions_ND(show=False)
        P_list = self.rasterize_conic(num=100, cone_parameters=cone_parameters, conic_parameters=conic_parameters)
        for P in P_list:
            ax.plot(*P.T, color='m')
        plt.show()

    def visualize_decision_surface_2D(self):
        conic_parameters = self.conic_parameters
        self.visualize_predictions_2D(show=False)
        plt.scatter(*self.exemplars_2D.Xp.T, color='g', s=10)

        P_list = self.rasterize_conic(num=100, conic_parameters=conic_parameters)
        for P in P_list:
            plt.plot(*P.T[:2], color='m')
        P_list = self.rasterize_conic(num=100, conic_parameters=self.circle_parameters)
        for P in P_list:
            plt.plot(*P.T[:2], color='g')
        plt.axis("equal")
        plt.show()
