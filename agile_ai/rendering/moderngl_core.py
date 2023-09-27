import moderngl
import numpy as np
from pyrr import Matrix44

from agile_ai.geometry.colored_mesh import ColoredMesh
from agile_ai.rendering.gl_core import GLCore
from agile_ai.rendering.moderngl_shaders import mvp_color
from agile_ai.rendering.opengl_unproject import unproject


class ModernGLCore(GLCore):
    def __init__(self):
        GLCore.__init__(self)
        self.P_image_opengl = np.eye(4)
        self.F_opengl_world = np.eye(4)
        self.last_indices = None

    def configure(self, z_near, z_far):
        GLCore.configure(self, z_near, z_far)

    def initialize(self, buffer_width, buffer_height):
        if self.initialized:
            return
        self.set_buffer_size(buffer_width, buffer_height)
        self.setup_gl_environment()
        self.setup_buffers(self.buffer_size)
        self.initialized = True
        self.mesh_data_of_index = dict()

    def clear_meshes(self):
        self.mesh_data_of_index = dict()
        self.last_indices = None

    def setup_gl_environment(self):
        self.ctx = moderngl.create_standalone_context()
        shader = mvp_color()
        self.prog = self.ctx.program(**shader)
        self.ctx.enable(moderngl.DEPTH_TEST)

    def setup_buffers(self, buffer_size):
        # self.ctx = moderngl.create_context()
        self.texture = self.ctx.texture(buffer_size, 3)
        depth_attachment = self.ctx.depth_texture(buffer_size)
        self.depth_attachement = depth_attachment
        self.fbo = self.ctx.framebuffer(self.texture, depth_attachment)

    def set_camera_size(self, width, height):
        self.width = width
        self.height = height
        self.fbo.viewport = (0, 0, width, height)

    def set_frustum(self, l, r, t, b, z_near, z_far):
        self.P_image_opengl = np.array(Matrix44.perspective_projection_bounds(l, r, t, b, z_near, z_far)).T
        M_image_world = self.P_image_opengl @ self.F_opengl_world
        self.set_projection_image_world(M_image_world)

    def set_projection_image_world(self, M_image_world):
        self.M_image_world = M_image_world
        self.mvp = self.prog['Mvp']
        self.mvp.write(M_image_world.T.astype('f4').tobytes())

    def render(self):
        self.fbo.clear(0, 0, 0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.fbo.use()
        self.texture.use()
        self.vao.render()

    def data(self, color=True, depth=True, xyz_camera=False, xyz_world=False):
        RGB = D = XYZ_camera = XYZ_world = None
        bw, bh = self.buffer_size
        w, h = self.width, self.height
        slc = slice(0, h), slice(0, w)
        if color:
            color_data = self.fbo.read(viewport=(0, 0, w, h))
            RGB = np.fromstring(color_data, dtype=np.uint8).reshape((h, w, -1))
        if depth or xyz_world or xyz_camera:
            depth_data = self.depth_attachement.read()
            D = np.fromstring(depth_data, dtype=np.float32).reshape((bh, bw))[slc]
            XYZ_camera, XYZ_world = unproject(self, D, xyz_camera=xyz_camera, xyz_world=xyz_world)
        return self.RenderedImages(RGB, D, XYZ_camera, XYZ_world)

    def set_modelview_matrix(self, F_opengl_world):
        self.F_opengl_world = F_opengl_world
        M_image_world = self.P_image_opengl @ self.F_opengl_world
        self.set_projection_image_world(M_image_world)


    def _populate_mesh_data_with_many_colors(self, mesh_data, triangles, triangle_colors):
        i = 0
        for X_world, colors in zip(triangles, triangle_colors):
            if colors.shape == (3,):
                colors = [colors, colors, colors]
            for X, C in zip(X_world, colors):
                mesh_data[i, :3] = X
                mesh_data[i:, 3:] = C
                i += 1

    def _populate_mesh_data_with_single_color(self, mesh_data, A, B, C, triangle_color):
        (Xa, Ya, Za), (Xb, Yb, Zb), (Xc, Yc, Zc) = A, B, C
        mesh_data[:, 3:] = triangle_color
        mesh_data[0::3, 0] = Xa
        mesh_data[0::3, 1] = Ya
        mesh_data[0::3, 2] = Za
        mesh_data[1::3, 0] = Xb
        mesh_data[1::3, 1] = Yb
        mesh_data[1::3, 2] = Zb
        mesh_data[2::3, 0] = Xc
        mesh_data[2::3, 1] = Yc
        mesh_data[2::3, 2] = Zc

    def add_mesh(self, colored_mesh: ColoredMesh, index):
        mesh = colored_mesh.mesh
        mesh_data = np.zeros((mesh.face_count * 3, 6), dtype="f4")
        if colored_mesh.is_one_color():
            triangle_color = colored_mesh.get_triangle_color(dtype=np.float32)
            A, B, C = mesh.get_triangle_vertices().transpose([1, 2, 0])
            self._populate_mesh_data_with_single_color(mesh_data, A, B, C, triangle_color / 255.0)
        else:
            triangle_colors = colored_mesh.get_triangle_colors()
            triangles = mesh.get_triangle_vertices()
            self._populate_mesh_data_with_many_colors(mesh_data, triangles, triangle_colors / 255.0)
        self.mesh_data_of_index[index] = mesh_data

    def get_viewport(self):
        return (0, 0, self.width, self.height)

    def render_indices(self, indices):
        if self.last_indices != indices:
            # Update data
            mesh_data = [self.mesh_data_of_index[index] for index in indices]
            mesh_data = np.vstack(mesh_data).astype("f4")
            self.vbo = self.ctx.buffer(mesh_data.tobytes())
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert', 'in_color')
            self.last_indices = indices
        self.render()

    def get_frame_opengl_world(self):
        return self.F_opengl_world

    def get_projection_matrix(self):
        return self.P_image_opengl
