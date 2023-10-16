from typing import List, NamedTuple

import numpy as np

from agile_ai.data_marshalling.numeric_types import FloatN
from agile_ai.geometry.colored_mesh import ColoredMesh
from agile_ai.geometry.pose_conversions import Rx, Ry, Rz
from agile_ai.geometry.shapes.cube import Cube
from agile_ai.geometry.shapes.planar import Plane
from agile_ai.geometry.shapes.sor import Sor, Sphere
from agile_ai.rendering.color_packer import ColorPacker
from agile_ai.rendering.renderer_interface import RendererInterface
from agile_ai.rendering.scene import Scene
from pynetest.expectations import expect


class TestContext:
    renderer: RendererInterface
    scene: Scene


def show_test_spheres(camera_params, F_camera_plane=None, axis=None):
    spheres = get_test_spheres()
    show_test_geometry(camera_params, F_camera_plane, axis, spheres)


def show_test_planes(camera_params, F_camera_plane=None, axis=None):
    planes = Plane.get_test_planes()
    show_test_geometry(camera_params, F_camera_plane, axis, planes)


def create_test_cases():
    from collections import OrderedDict
    cases = OrderedDict()
    # Natural camera
    cases["natural"] = ((1, 1, 0, 0, 2, 2), None, (-1, 1, 1, -1))
    # Natural focus, shifted center
    camera_params = (1, 1, 1, 1, 2, 2)
    cases["natural_shifted"] = (camera_params, None, None)
    # Square pixel camera, zoomed out slightly
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    cases["square_pixel"] = (camera_params, None, None)
    # Tall pixel camera
    w = h = 500
    fx = 200
    fy = 250
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    cases["tall_pixel"] = (camera_params, None, None)
    # Wide pixel camera
    w = h = 500
    fx = 250
    fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    cases["wide_pixel"] = (camera_params, None, None)
    # Square pixel camera, zoomed out slightly, off center v
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0 + 50
    camera_params = (fx, fy, cx, cy, w, h)
    cases["off_center_v"] = (camera_params, None, None)
    # Square pixel camera, zoomed out slightly, off center u
    w = h = 500
    fx = fy = 200
    cx = w / 2.0 + 50
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    cases["off_center_u"] = (camera_params, None, None)
    # Slighted rotated plane around Rx
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Rx(.2)
    cases["rotated_x"] = (camera_params, F_camera_plane, None)
    # Slighted rotated plane around Ry
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Ry(.2)
    cases["rotated_y"] = (camera_params, F_camera_plane, None)
    # Slighted rotated plane around Rz
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Rz(.2)
    cases["rotated_z"] = (camera_params, F_camera_plane, None)
    # Slighted translated plane around Rx
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Rx(.2)
    F_camera_plane[:3, -1] = (0.5, 0, 0)
    cases["translated_x"] = (camera_params, F_camera_plane, None)
    # Slighted translated plane around Ry
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Rx(.2)
    F_camera_plane[:3, -1] = (0, .5, 0)
    cases["translated_y"] = (camera_params, F_camera_plane, None)
    # Slighted translated plane around Rz
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, :3] = Rx(.2)
    F_camera_plane[:3, -1] = (0, 0, .5)
    cases["translated_z"] = (camera_params, F_camera_plane, None)
    # Slighted sm_translated plane around Rx
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, -1] = (0.25, 0, 0)
    cases["sm_translated_x"] = (camera_params, F_camera_plane, None)
    # Slighted sm_translated plane around Ry
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, -1] = (0, .25, 0)
    cases["sm_translated_y"] = (camera_params, F_camera_plane, None)
    # Slighted sm_translated plane around Rz
    w = h = 500
    fx = fy = 200
    cx = w / 2.0
    cy = h / 2.0
    camera_params = (fx, fy, cx, cy, w, h)
    F_camera_plane = np.eye(4)
    F_camera_plane[:3, -1] = (0, 0, .25)
    cases["sm_translated_z"] = (camera_params, F_camera_plane, None)
    return cases


def show_test(name, planes=True):
    params = test_cases[name]
    if planes:
        show_test_planes(*params)
    else:
        show_test_spheres(*params)


def show_tests(planes=True):
    for name in test_cases.keys():
        show_test(name, planes)
        input(name)


def mask_erosion_match(Mexp, Mren, iterations=2):
    from scipy.ndimage import binary_erosion
    Mexp = binary_erosion(Mexp, iterations=iterations)
    ren_count = Mren[Mexp].sum()
    exp_count = Mexp.sum()
    diff_count = exp_count - ren_count
    return exp_count, ren_count, diff_count


def expect_depth_mask_match(tc: TestContext, name):
    camera_geometry, F_camera_world = test_cases[name][:2]
    tc.scene.set_camera_geometry(*camera_geometry)
    if F_camera_world is None:
        F_camera_world = np.eye(4)
    tc.scene.set_frame_camera_world(F_camera_world)
    tc.renderer.render()
    exp_image = get_test_case_image(name)[0]
    ren_depth = tc.renderer.get_data(color=False, depth=True).depth
    Mexp = exp_image.any(2)
    Mren = (ren_depth < 1)
    exp_count, ren_count, diff_count = mask_erosion_match(Mexp, Mren)
    if diff_count != 0:
        import imageio
        imageio.imsave("exp_image.png", (Mexp * 255).astype(np.uint8))
        imageio.imsave("ren_image.png", (Mren * 255).astype(np.uint8))
    expect(ren_count).to_be(exp_count)


def expect_z_mask_match(tc: TestContext, name):
    camera_geometry, F_camera_world = test_cases[name][:2]
    tc.renderer.set_camera_geometry(*camera_geometry)
    if F_camera_world is None:
        F_camera_world = np.eye(4)
    tc.renderer.set_frame_camera_world(F_camera_world)
    tc.renderer.render()
    exp_image, exp_uv, exp_xyz = get_test_case_image(name)
    Zren = tc.renderer.get_data(color=False, depth=False, xyz_world=True).xyz_world[2]
    Mexp = exp_image.any(2)
    Mren = (Zren > 0)
    exp_count, ren_count, diff_count = mask_erosion_match(Mexp, Mren)
    if diff_count != 0:
        import imageio
        imageio.imsave("exp_image.png", (Mexp * 255).astype(np.uint8))
        imageio.imsave("ren_image.png", (Mren * 255).astype(np.uint8))
    expect(ren_count).to_be(exp_count)


def expect_xyz_world_match(tc: TestContext, name):
    camera_geometry, F_camera_world = test_cases[name][:2]
    tc.scene.set_camera_geometry(*camera_geometry)
    if F_camera_world is None:
        F_camera_world = np.eye(4)
    else:
        F_camera_world = F_camera_world.copy()
    tc.scene.set_frame_camera_world(F_camera_world)
    tc.renderer.render()
    # TODO XYZ_exp should be XYZ_world, its currently camera
    color_exp, (U_exp, V_exp), XYZ_camera_exp, XYZ_world_exp = get_test_case_spheres_image(name, z_min=.05)
    data = tc.renderer.get_data(color=True, depth=False, xyz_world=True, xyz_camera=True)
    color_ren = data.color
    xyz_ren = data.xyz_world
    RGB_ren = color_ren[V_exp, U_exp]
    RGB_exp = color_exp[V_exp, U_exp]
    XYZ_world_ren = data.xyz_world[V_exp, U_exp]
    XYZ_camera_ren = data.xyz_camera[V_exp, U_exp]
    for u, v, rgb_exp, rgb_ren in zip(U_exp, V_exp, RGB_exp, RGB_ren):
        expect((u, v) + tuple(rgb_ren)).to_be((u, v) + tuple(rgb_exp))
    for u, v, xyz_exp, xyz_ren in zip(U_exp, V_exp, XYZ_camera_exp, XYZ_camera_ren):
        diff = np.linalg.norm(xyz_exp - xyz_ren)
        expect(np.linalg.norm(xyz_exp - xyz_ren) < .015).to_be(True)
    for u, v, xyz_exp, xyz_ren in zip(U_exp, V_exp, XYZ_world_exp, XYZ_world_ren):
        diff = np.linalg.norm(xyz_exp - xyz_ren)
        expect(np.linalg.norm(xyz_exp - xyz_ren) < .015).to_be(True)

    expect(len(RGB_exp) > 0).to_be(True)
    return


def get_test_case_spheres_image(name, z_min=.01):
    camera_params, F_camera_plane = test_cases[name][:2]
    return create_spheres_test_image(camera_params, F_camera_plane, z_min=z_min)


def get_test_case_image(name, visibilities=None):
    camera_params, F_camera_plane = test_cases[name][:2]
    return create_test_geometry_image(camera_params, F_camera_plane, visibilities)


def create_spheres_test_image(camera_params, F_camera_plane=None, z_min=.01):
    spheres = get_test_spheres()
    return render_image_cv(camera_params, F_camera_plane, spheres, z_min=z_min)


def create_test_geometry_image(camera_params, F_camera_plane=None, visibilities=None):
    planes = get_test_planes()
    if visibilities is None:
        visibilities = [True, True, True, True]
    planes = [p for (p, v) in zip(planes, visibilities) if v]
    return render_image_cv(camera_params, F_camera_plane, planes)


def render_image_cv(camera_params, F_camera_world, meshes, z_min=.01):
    import cv2
    fx, fy, cx, cy, w, h = camera_params
    K = np.array([(fx, 0, cx), (0, fy, cy), (0, 0, 1)])
    color_image = np.zeros((h, w, 3), dtype=np.uint8)
    uv_points = []
    xyz_camera_points = []
    xyz_world_points = []
    if F_camera_world is None:
        F_camera_world = np.eye(4)
    R_camera_world = F_camera_world[:3, :3]
    t_camera_world = F_camera_world[:3, -1][:, None]
    for mesh in meshes:
        means = []
        for X_world, color in zip(mesh.get_triangle_vertices(), mesh.get_triangle_colors()):
            X_camera = R_camera_world @ X_world.T + t_camera_world
            xyz_c_mean = X_camera.mean(1)
            xyz_w_mean = X_world.T.mean(1)
            X_image = K @ X_camera
            Z = X_image[-1]
            if Z.mean() < z_min:
                continue
            X_image = (X_image[:2] / Z).astype(int).T
            color = tuple([int(c) for c in color])
            cv2.fillPoly(color_image, [X_image], color)
            u, v = uv_mean = X_image.mean(0)
            if u < 0 or v < 0 or u >= w or v >= h:
                continue
            means.append((uv_mean, xyz_c_mean, xyz_w_mean))
        if means:
            uv_means, xyz_c_means, xyz_w_means = zip(*means)
            xyz_camera_points.append(np.mean(xyz_c_means, axis=0))
            xyz_world_points.append(np.mean(xyz_w_means, axis=0))
            uv_points.append(np.mean(uv_means, axis=0))
    uv_points = np.array(uv_points, dtype=int)
    uv_points = tuple(uv_points.T[0]), tuple(uv_points.T[1])
    xyz_camera_points = np.array(xyz_camera_points)
    return color_image, uv_points, xyz_camera_points, xyz_world_points


def expect_image_match(tc: TestContext, name, visibilities=None):
    camera_geometry, F_camera_world = test_cases[name][:2]
    tc.scene.set_camera_geometry(*camera_geometry)
    if F_camera_world is None:
        F_camera_world = np.eye(4)
    tc.scene.set_frame_camera_world(F_camera_world)
    tc.renderer.render()
    exp_image = get_test_case_image(name, visibilities)[0]
    ren_image = tc.renderer.get_data().color
    exp_image_code = ColorPacker.pack(exp_image.transpose((2, 0, 1)))
    ren_image_code = ColorPacker.pack(ren_image.transpose((2, 0, 1)))
    diff_count = (exp_image != ren_image).any(2).sum()
    codes = set(np.unique(ren_image_code)) | set(np.unique(exp_image_code))
    codes.discard(0)
    for code in codes:
        Mexp = (exp_image_code == code)
        Mren = (ren_image_code == code)
        exp_count, ren_count, diff_count = mask_erosion_match(Mexp, Mren)
        expect(ren_count).to_be(exp_count)

    if diff_count and VISUALIZE:
        import pylab
        pylab.imshow(exp_image)
        pylab.title("Expected image")
        pylab.show()
        pylab.imshow(ren_image)
        pylab.title("Rendered image")
        pylab.show()

    expect(diff_count).to_be(0)


VISUALIZE = False


class TestSphereCollection(NamedTuple):
    radii: FloatN
    heights: FloatN
    sphere: Sphere
    cube_list: List[Cube]


def get_test_sphere_collection() -> TestSphereCollection:
    n_heights = 18
    n_thetas = 16
    radii = np.sin(np.linspace(0, np.pi, n_heights)[1:-1]) / 2.0
    heights = np.cos(np.linspace(np.pi, 0, n_heights))[1:-1] / 2.0
    sphere = Sor(heights, radii, n_thetas)
    cube_list = []
    for i, v in enumerate(sphere.vertices):
        cube = Cube()
        cube.scale(.0075)
        cube.translate(v)
        cube.center = v
        name = "cube_%0.6d" % i
        cube.with_name(name)
        cube_list.append(cube)
    return TestSphereCollection(radii=radii,
                                heights=heights,
                                sphere=sphere,
                                cube_list=cube_list)


# @fun_memo
def get_test_spheres() -> List[ColoredMesh]:
    max_color_code = ColorPacker.pack((255, 255, 255))
    min_color_code = ColorPacker.pack((0, 0, 255))
    collection = get_test_sphere_collection()
    color_codes = np.linspace(min_color_code, max_color_code, len(collection.cube_list)).astype(int)
    colors = np.array(ColorPacker.unpack(color_codes)).T.astype(np.uint8)
    colored_mesh_list = []
    for mesh, color in zip(collection.cube_list, colors):
        colored_mesh = ColoredMesh(mesh, triangle_color=color)
        colored_mesh_list.append(colored_mesh)
    return colored_mesh_list


def show_test_geometry(camera_params, F_camera_geometry, axis, geometry):
    import pylab
    fx, fy, cx, cy, w, h = camera_params
    K = np.array([(fx, 0, cx), (0, fy, cy), (0, 0, 1)])
    if axis is None:
        axis = (0, w, h, 0)
    pylab.clf()
    ax = pylab.gca()
    for geo in geometry:
        if F_camera_geometry is not None:
            R_camera_geometry = F_camera_geometry[:3, :3]
            t_camera_geometry = F_camera_geometry[:3, -1]
            geo.rotate_XYZ(R_camera_geometry)
            geo.translate(t_camera_geometry)
        for vs, color in zip(geo.triangles, geo.triangle_colors):
            vs = (K @ vs.T)
            Z = vs[-1]
            if (Z < .01).any():
                continue
            vs /= Z
            vs = vs.T
            color = np.array(color, dtype=float) / 255
            poly = pylab.Polygon(vs[:, :2], fill=True, color=color)
            ax.add_patch(poly)
    ax.axis(axis)
    pylab.gcf().canvas.draw()


def get_test_planes() -> List[ColoredMesh]:
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
    plane_y = ColoredMesh(plane.copy(), (255, 255, 0))
    # plane_g (-1, 0, 1) --- (0, 1, 1)
    plane_g = ColoredMesh(plane.copy(), (0, 255, 0))
    plane_g.mesh.translate((-1, 0, 0))
    # plane_r (-1, -1, 1) --- (0, 0, 1)
    plane_r = ColoredMesh(plane.copy(), (255, 0, 0))
    plane_r.mesh.translate((-1, -1, 0))
    # plane_b (0, -1, 1) --- (1, 0, 1)
    plane_b = ColoredMesh(plane.copy(), (0, 0, 255))
    plane_b.mesh.translate((0, -1, 0))
    return [plane_r, plane_g, plane_b, plane_y]


test_cases = create_test_cases()
