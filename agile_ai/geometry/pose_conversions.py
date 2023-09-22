import logging
from collections import namedtuple
from typing import Union

import numpy as np

from avvir_dataflow.utils.numeric_types import Float44, Float4, Float33

FrameTuple = namedtuple("FrameTuple", "R t")


def average_rotations(rotations):
    Ravg = np.zeros((3, 3))
    for R in rotations:
        Ravg += R
    Ravg /= float(len(rotations))
    U, S, V = np.linalg.svd(Ravg)
    Ravg = np.dot(U, V)
    Ravg[2] *= np.linalg.det(Ravg)
    assert (np.isclose(np.linalg.det(Ravg), 1))
    return Ravg


def average_transforms(transforms):
    Favg = np.zeros((4, 4))
    for F in transforms:
        Favg += F
    Favg /= float(len(transforms))
    Ravg, tavg = frame_to_rotation_translation(Favg)
    U, S, V = np.linalg.svd(Ravg)
    Ravg = np.dot(U, V)
    Favg = rotation_translation_to_frame(Ravg, tavg)
    # Ferror = np.zeros((4,4))
    # for F in transforms:
    #  Ferror += (F-Favg)
    # Ferror /= len(transforms)
    # print Ferror
    return Favg


def point_vector_to_homogeneous_line(point, vector):
    # The input non-homogeneous line is described by a point and a vector
    # A homogenous line describes a plane containing the non-homogenous line and the center of projection
    # The simplest conversion is the cross product of two points.
    # Alternatively, two points can be projected onto z=1, and the resulting vector computed
    # This vector can be interpreted as a 2D normal in the plane z=1
    # Then, the offset d can be calculated such that Nx + d = 0

    # P1 = X = <x,y,z>
    # P2 = X + qV = <x,y,z> + q<a,b,c>
    # P1' = X/z
    # P2' = (X + qV) / (z + qc)
    # V' = P2' - P1' = [(X+qV)/(z+qc)] - [X/z]
    # V' = [z(X+qV)/(z(z+qc))] - [(X(z+qc)/(z(z+qc))]
    # V' ~ z(X+qV) - X(z+qc)
    # V' ~ Xz - qVz - Xz + Xqc
    # V' ~ qVz - qXc
    # V' ~ Vz - Xc
    # V' ~ V- Xc/z
    # V' ~ V/c - X/z

    # Method one: Cross Product
    p1 = point
    p2 = point + vector
    line = np.cross(p1, p2)
    line /= np.linalg.norm(line[:2]) * np.sign(line[0])  # Not necessary
    return line

    # Method two: Projection
    # Project the vector onto the plane z. The result is dependent on point!
    v_proj = vector[:2] / vector[-1] - point[:2] / point[-1]
    v_proj /= np.linalg.norm(v_proj) * np.sign(v_proj[0])
    a, b = v_proj

    # Project the point onto the plane z = 1, dividing by z
    x, y = point[:2] / point[-1]

    # Treat the vector as a normal in the plane z = 1,
    na = b
    nb = -a

    # Solve the offset that satisifes Nx = 0
    d = -(na * x + nb * y)
    line = np.array((na, nb, d))
    line /= np.linalg.norm(line[:2]) * np.sign(line[0])  # Not necessary
    return line


def frame_to_x_axis_homogeneous_line(frame):
    R, t = pc.RT(frame)
    x_axis, y_axs, z_axis = R.T
    center = t
    return point_vector_to_homogeneous_line(x_axis, center)


def frame_to_y_axis_homogeneous_line(frame):
    R, t = pc.RT(frame)
    x_axis, y_axs, z_axis = R.T
    center = t
    return point_vector_to_homogeneous_line(y_axis, center)


def frame_to_z_axis_homogeneous_line(frame):
    R, t = pc.RT(frame)
    x_axis, y_axs, z_axis = R.T
    center = t
    return point_vector_to_homogeneous_line(z_axis, center)


def homogenize(P, column=True, zero_pad=False):
    # Column means column vectors, 3xn
    nr, nc = P.shape
    if column:
        shape = (nr + 1, nc)
        Ph = np.zeros(shape) if zero_pad else np.ones(shape)
        Ph[:nr] = P
        return Ph
    else:
        return homogenize(P.T, zero_pad=zero_pad).T


def dehomogenize(Ph, column=True):
    # Column means column vectors, 3xn
    if column:
        return Ph[:-1] / Ph[-1]
    else:
        return dehomogenize(Ph.T).T


def frame_to_homography(frame):
    # Create homography, drop the z column and remove the last row
    return frame[:3, [0, 1, 3]].copy()


def ensure_rotation(R_a_to_b):
    det = np.linalg.det(R_a_to_b)
    eye = R_a_to_b @ R_a_to_b.T
    print("det  :", det)
    print("eye  :\n", eye)
    assert np.isclose(det, 1.0)
    assert np.isclose(eye, np.eye(3)).all()


def ensure_rigid_transform(F_a_to_b, skip_scale=False):
    R_a_to_b, t_a_to_b = frame_to_rotation_translation(F_a_to_b)
    det = np.linalg.det(R_a_to_b)
    eye = R_a_to_b @ R_a_to_b.T
    scale = F_a_to_b[-1, -1]
    zeros = F_a_to_b[-1, :3]
    if not skip_scale:
        print("scale:", scale)
    print("det  :", det)
    print("eye  :\n", eye)
    print("zeros:", scale)
    assert np.isclose(det, 1.0)
    assert np.isclose(eye, np.eye(3)).all()
    if not skip_scale:
        assert np.isclose(scale, 1)
    assert np.isclose(zeros, 0).all()


def ensure_similarity_transform(similarity):
    similarity = similarity.copy()
    scale = similarity[-1, -1]
    print("scale:", scale)
    similarity[-1, -1] = 1.0
    ensure_rigid_transform(similarity, skip_scale=True)


def apply(*args):
    args = args[::-1]
    result = M(args[0])
    args = args[1:]
    try:
        for arg in args:
            if isinstance(arg, str):
                if arg == 'h':
                    result = homogenize(result)
                elif arg == 'hz':
                    result = homogenize(result, zero_pad=True)
                elif arg == 'd':
                    result = dehomogenize(result)
                elif arg == 'i':
                    result = np.linalg.inv(result)
                elif arg == 'u':  # Upgrade dimension, eg, 3x3->4x4, adding eye ones
                    nr, nc = result.shape
                    add = result
                    result = np.zeros((nr + 1, nc + 1))
                    result[nr, nc] = 1
                    result[:nr, :nc] += add
                elif arg == 'r':  # Reduce dimension, eg, 4x4->3x3
                    nr, nc = result.shape
                    result = result[:nr - 1, :nc - 1].copy()
                elif arg == "dz":
                    result = result[:-1]
                elif arg == "H":  # Create homography, drop the z column and remove the last row
                    result = result[:3, [0, 1, 3]].copy()
            else:
                result = np.dot(M(arg), result)
    except ValueError as e:
        logging.error(arg, exc_info=e)
        logging.error(result)
        logging.error(f"{arg.shape}, {result.shape}")

    return result


def get_K(K):
    try:
        return np.array(K.P).reshape(3, 4)
    except:
        return K


def invert(pose):
    R, t = frame_to_rotation_translation(pose)
    Rinv = R.T
    tinv = -np.dot(R.T, t)
    return rotation_translation_to_frame(Rinv, tinv)


def Ry(theta, homogenous=False):
    R = np.eye(3)
    R[0, 0] = np.cos(theta)
    R[0, 2] = np.sin(theta)
    R[2, 0] = -np.sin(theta)
    R[2, 2] = np.cos(theta)
    return apply('u', R) if homogenous else R


def Rx(theta, homogenous=False):
    R = np.eye(3)
    R[1, 1] = np.cos(theta)
    R[1, 2] = -np.sin(theta)
    R[2, 1] = np.sin(theta)
    R[2, 2] = np.cos(theta)
    return apply('u', R) if homogenous else R


def Rz(theta, homogenous=False):
    R = np.eye(3)
    R[0, 0] = np.cos(theta)
    R[0, 1] = -np.sin(theta)
    R[1, 0] = np.sin(theta)
    R[1, 1] = np.cos(theta)
    return apply('u', R) if homogenous else R


def align_axis(old_axis, new_axis):
    r_axis = np.cross(old_axis, new_axis)
    theta = np.arccos(np.dot(old_axis, new_axis))
    return Raxis(r_axis, theta)


def matrix_to_quaternion(matrix: Union[Float44, Float33], isprecise=False) -> Float4:
    """
    If isprecise is True, the input matrix is assumed to be a precise rotation
    matrix and a faster algorithm is used.
    https://www.lfd.uci.edu/~gohlke/code/transformations.py.html
    """
    w, x, y, z = _matrix_to_quaternion(matrix, isprecise)
    return np.array([x, y, z, w])


def _matrix_to_quaternion(matrix: Union[Float44, Float33], isprecise=False) -> Float4:
    """Return quaternion from rotation matrix.
    The output quaternion's definition is ordered as w, x, y, z

    If isprecise is True, the input matrix is assumed to be a precise rotation
    matrix and a faster algorithm is used.
    https://www.lfd.uci.edu/~gohlke/code/transformations.py.html

    >>> q = quaternion_from_matrix(np.identity(4), True)
    >>> np.allclose(q, [1, 0, 0, 0])
    True
    >>> q = quaternion_from_matrix(np.diag([1, -1, -1, 1]))
    >>> np.allclose(q, [0, 1, 0, 0]) or np.allclose(q, [0, -1, 0, 0])
    True
    >>> R = rotation_matrix(0.123, (1, 2, 3))
    >>> q = quaternion_from_matrix(R, True)
    >>> np.allclose(q, [0.9981095, 0.0164262, 0.0328524, 0.0492786])
    True
    >>> R = [[-0.545, 0.797, 0.260, 0], [0.733, 0.603, -0.313, 0],
    ...      [-0.407, 0.021, -0.913, 0], [0, 0, 0, 1]]
    >>> q = quaternion_from_matrix(R)
    >>> np.allclose(q, [0.19069, 0.43736, 0.87485, -0.083611])
    True
    >>> R = [[0.395, 0.362, 0.843, 0], [-0.626, 0.796, -0.056, 0],
    ...      [-0.677, -0.498, 0.529, 0], [0, 0, 0, 1]]
    >>> q = quaternion_from_matrix(R)
    >>> np.allclose(q, [0.82336615, -0.13610694, 0.46344705, -0.29792603])
    True
    >>> R = random_rotation_matrix()
    >>> q = quaternion_from_matrix(R)
    >>> is_same_transform(R, quaternion_matrix(q))
    True
    >>> is_same_quaternion(quaternion_from_matrix(R, isprecise=False),
    ...                    quaternion_from_matrix(R, isprecise=True))
    True
    >>> R = euler_matrix(0.0, 0.0, np.pi/2.0)
    >>> is_same_quaternion(quaternion_from_matrix(R, isprecise=False),
    ...                    quaternion_from_matrix(R, isprecise=True))
    True

    """
    M = np.array(matrix, dtype=np.float64, copy=False)[:4, :4]
    if isprecise:
        q = np.empty((4,))
        t = np.trace(M)
        if t > M[3, 3]:
            q[0] = t
            q[3] = M[1, 0] - M[0, 1]
            q[2] = M[0, 2] - M[2, 0]
            q[1] = M[2, 1] - M[1, 2]
        else:
            i, j, k = 0, 1, 2
            if M[1, 1] > M[0, 0]:
                i, j, k = 1, 2, 0
            if M[2, 2] > M[i, i]:
                i, j, k = 2, 0, 1
            t = M[i, i] - (M[j, j] + M[k, k]) + M[3, 3]
            q[i] = t
            q[j] = M[i, j] + M[j, i]
            q[k] = M[k, i] + M[i, k]
            q[3] = M[k, j] - M[j, k]
            q = q[[3, 0, 1, 2]]
        q *= 0.5 / np.sqrt(t * M[3, 3])
    else:
        m00 = M[0, 0]
        m01 = M[0, 1]
        m02 = M[0, 2]
        m10 = M[1, 0]
        m11 = M[1, 1]
        m12 = M[1, 2]
        m20 = M[2, 0]
        m21 = M[2, 1]
        m22 = M[2, 2]
        # symmetric matrix K
        K = np.array([[m00 - m11 - m22, 0.0, 0.0, 0.0],
                      [m01 + m10, m11 - m00 - m22, 0.0, 0.0],
                      [m02 + m20, m12 + m21, m22 - m00 - m11, 0.0],
                      [m21 - m12, m02 - m20, m10 - m01, m00 + m11 + m22]])
        K /= 3.0
        # quaternion is eigenvector of K that corresponds to largest eigenvalue
        w, V = np.linalg.eigh(K)
        q = V[[3, 0, 1, 2], np.argmax(w)]
    if q[0] < 0.0:
        np.negative(q, q)
    return q


def quaternion_to_matrix(x: float, y: float, z: float, w: float) -> Float33:
    return _quaternion_to_matrix(np.array([w, x, y, z]))[:3, :3]


def _quaternion_to_matrix(quaternion: Float4) -> Float44:
    """Return homogeneous rotation matrix from quaternion.
    The expected definition of a quaternion in this context is w, x, y, z
    >>> M = quaternion_matrix([0.99810947, 0.06146124, 0, 0])
    >>> numpy.allclose(M, rotation_matrix(0.123, [1, 0, 0]))
    True
    >>> M = quaternion_matrix([1, 0, 0, 0])
    >>> numpy.allclose(M, numpy.identity(4))
    True
    >>> M = quaternion_matrix([0, 1, 0, 0])
    >>> numpy.allclose(M, numpy.diag([1, -1, -1, 1]))
    True

    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    n = np.dot(q, q)
    if n < 1e-8:
        return np.identity(4)
    q *= np.sqrt(2.0 / n)
    q = np.outer(q, q)
    return np.array([
        [1.0 - q[2, 2] - q[3, 3], q[1, 2] - q[3, 0], q[1, 3] + q[2, 0], 0.0],
        [q[1, 2] + q[3, 0], 1.0 - q[1, 1] - q[3, 3], q[2, 3] - q[1, 0], 0.0],
        [q[1, 3] - q[2, 0], q[2, 3] + q[1, 0], 1.0 - q[1, 1] - q[2, 2], 0.0],
        [0.0, 0.0, 0.0, 1.0]])


def Raxis(axis, theta):
    from scipy.linalg import expm
    return expm(np.cross(np.eye(3), axis / np.linalg.norm(axis) * theta))


def similarity_to_rotation_translation(frame):
    if isinstance(frame, tuple):
        return frame
    rotation = frame[:3, :3]
    translation = frame[:3, 3] / frame[3, 3]
    return rotation, translation


def similarity_to_rotation_translation_scale(frame):
    if isinstance(frame, tuple):
        return frame
    rotation = frame[:3, :3]
    translation = frame[:3, 3]
    scale = 1.0 / frame[3, 3]
    return rotation, translation, scale


def frame_to_rotation_translation(frame):
    if isinstance(frame, tuple):
        return frame
    rotation = frame[:3, :3]
    translation = frame[:3, 3]
    return rotation, translation


def rotation_translation_to_frame(rotation, translation):
    frame = np.eye(4)
    frame[:3, :3] = rotation
    frame[:3, 3] = translation
    return frame


def invert_frame(frame):
    R, t = frame_to_rotation_translation(frame)
    Rinv = R.T
    tinv = -np.dot(R.T, t)
    return rotation_translation_to_frame(Rinv, tinv)


def invert_rotation_translation(rotation, translation):
    Rinv = rotation.T
    tinv = -np.dot(rotation.T, translation)
    return Rinv, tinv


def change_rotation_axes(old_x_axis, old_y_axis, old_z_axis, new_x_axis, new_y_axis, new_z_axis):
    R_old_to_basis = np.array((old_x_axis, old_y_axis, old_z_axis))
    R_new_to_basis = np.array((new_x_axis, new_y_axis, new_z_axis))
    R_basis_to_new = R_new_to_basis.T
    R_old_to_new = R_basis_to_new @ R_old_to_basis
    return R_old_to_new


def normed(vector):
    return vector / np.linalg.norm(vector)


def signed_angle(normal, vector_1, vector_2):
    unit_1 = vector_1 / np.linalg.norm(vector_1)
    unit_2 = vector_2 / np.linalg.norm(vector_2)
    unsigned_angle = np.arccos(unit_1 @ unit_2)

    if norm_cross(unit_1, unit_2) @ normal < 0:
        return -unsigned_angle
    else:
        return +unsigned_angle


def norm_cross(va, vb):
    vc = np.cross(va, vb)
    vc /= np.linalg.norm(vc)
    return vc
