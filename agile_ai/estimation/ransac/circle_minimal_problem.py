import numpy as np


def solve(A_xy, B_xy, C_xy):
    # (x_a-x_0)**2 + (y_a-y_0)**2 = r**2
    # --
    # x_a**2 - 2(x_a)(x_0) + x_0**2 + y_a**2 - 2(y_a)(y_0) + y_0**2 = r**2
    # x_b**2 - 2(x_b)(x_0) + x_0**2 + y_b**2 - 2(y_b)(y_0) + y_0**2 = r**2
    # x_c**2 - 2(x_c)(x_0) + x_0**2 + y_c**2 - 2(y_c)(y_0) + y_0**2 = r**2
    # --
    # [x_a**2 - 2(x_a)(x_0) + x_0**2] + [y_a**2 - 2(y_a)(y_0) + y_0**2] = r**2
    # [x_c**2 - 2(x_c)(x_0) + x_0**2] + [y_c**2 - 2(y_c)(y_0) + y_0**2] = r**2
    # --
    # [x_a**2 - 2(x_a)(x_0)] - [x_c**2 - 2(x_c)(x_0)] + [y_a**2 - 2(y_a)(y_0)] - [y_c**2 - 2(y_c)(y_0)] = 0
    # [x_a**2 - x_c**2] - [2(x_a) + 2(x_c)] (x_0) + [y_a**2 - y_c**2] - [2(y_a) + 2(y_c)] (y_0) = 0
    # Uac_x + Vac_x (x_0) + Uac_y + Vac_y (y_0) = 0
    # Uac + Vac_x (x_0) + Vac_y (y_0) = 0
    # --
    # Uac + Vac_x (x_0) + Vac_y (y_0) = 0
    # Ubc + Vbc_x (x_0) + Vbc_y (y_0) = 0
    # --
    # Uac (Vbc_x) + Vac_x (Vbc_x) (x_0) + Vac_y (Vbc_x) (y_0) = 0
    # Ubc (Vac_x) + Vac_x (Vbc_x) (x_0) + Vac_x (Vbc_y) (y_0) = 0
    # ... Uac (Vbc_x) - Ubc (Vac_x) + [Vac_y (Vbc_x) - Vac_x (Vbc_y)] (y_0) = 0
    # Uac (Vbc_y) + Vac_x (Vbc_y) (x_0) + Vac_y (Vbc_y) (y_0) = 0
    # Ubc (Vac_y) + Vbc_x (Vac_y) (x_0) + Vac_y (Vbc_y) (y_0) = 0
    # ... Uac (Vbc_y) - Ubc (Vac_y) + [Vac_x (Vbc_y) - Vbc_x (Vac_y)] (x_0) = 0
    X_a, Y_a = A_xy.T.astype(np.float64)
    X_b, Y_b = B_xy.T.astype(np.float64)
    X_c, Y_c = C_xy.T.astype(np.float64)
    # --
    Uac_x = X_a ** 2 - X_c ** 2
    Uac_y = Y_a ** 2 - Y_c ** 2
    Vac_x = 2 * (X_c - X_a)
    Vac_y = 2 * (Y_c - Y_a)
    Uac = Uac_x + Uac_y
    Ubc_x = X_b ** 2 - X_c ** 2
    Ubc_y = Y_b ** 2 - Y_c ** 2
    Vbc_x = 2 * (X_c - X_b)
    Vbc_y = 2 * (Y_c - Y_b)
    Ubc = Ubc_x + Ubc_y
    # ... Uac (Vbc_x) - Ubc (Vac_x) + [Vac_y (Vbc_x) - Vac_x (Vbc_y)] (y_0) = 0
    # ... Uac (Vbc_y) - Ubc (Vac_y) + [Vac_x (Vbc_y) - Vbc_x (Vac_y)] (x_0) = 0
    My = Uac * Vbc_x - Ubc * Vac_x
    Mx = Uac * Vbc_y - Ubc * Vac_y
    Ny = Vac_y * Vbc_x - Vac_x * Vbc_y
    Nx = Vac_x * Vbc_y - Vbc_x * Vac_y
    # ... My + Ny * y_0 = 0
    # ... Mx + Nx * x_0 = 0
    Y0 = -My / Ny
    X0 = -Mx / Nx
    R = np.sqrt((X_a - X0)**2 + (Y_a - Y0)**2)
    P = np.array((X0, Y0)).T
    return P, R
