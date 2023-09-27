import numpy as np


def unproject(self, depth, xyz_camera, xyz_world):
    XYZ_camera = XYZ_world = None
    if xyz_world or xyz_camera:
        viewport = self.get_viewport()
        X_image, valid = unproject_to_image(depth, viewport)
    if xyz_world:
        F_opengl_world = self.get_frame_opengl_world()
        XYZ_world = unproject_to_system(self, X_image, valid, F_opengl_world)
    if xyz_camera:
        F_opengl_camera = self.F_opengl_camera
        XYZ_camera = unproject_to_system(self, X_image, valid, F_opengl_camera)
    return XYZ_camera, XYZ_world


def unproject_to_system(self, X_image, valid, F_opengl_system):
    shape = valid.shape
    XYZ = np.zeros((shape[0], shape[1], 3))
    P_image_opengl = self.get_projection_matrix()
    Xv, Yv, Zv = unproject_image_to_system(X_image,
                                           P_image_opengl,
                                           F_opengl_system).T
    XYZ[valid, 0] = Xv
    XYZ[valid, 1] = Yv
    XYZ[valid, 2] = Zv
    return XYZ


def unproject_to_image(depth, viewport):
    # Transformation of normalized coordinates between -1 and 1
    shape = depth.shape
    U, V = np.meshgrid(range(shape[1]), range(shape[0]))
    valid = depth != 1
    U = U[valid].astype(float)
    V = V[valid].astype(float)
    D = depth[valid]
    Nx = (U - viewport[0]) / viewport[2] * 2.0 - 1.0
    Ny = (V - viewport[1]) / viewport[3] * 2.0 - 1.0
    Nz = 2.0 * D - 1.0
    Nw = np.ones_like(Nx)
    X_image = np.array((Nx, Ny, Nz, Nw))
    return X_image, valid


def unproject_image_to_system(X_image, P_image_opengl, F_opengl_system):
    M_image_system = np.dot(P_image_opengl, F_opengl_system)
    M_system_image = np.linalg.inv(M_image_system)
    X_system = np.dot(M_system_image, X_image)
    X_system[:3] /= X_system[3]
    return X_system[:3].T
