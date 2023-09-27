import numpy as np
from OpenGL import GL, GLUT
from OpenGL.GL import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GLUT import *

from .gl_core import GLCore
from .opengl_unproject import unproject


# flake8: noqa
# pylint: skip-file

class OpenGLCore(GLCore):
    def __init__(self, buffer_width, buffer_height, z_near, z_far):
        GLCore.__init__(self, buffer_width, buffer_height, z_near, z_far)
        self.window_handle = None

    def initialize(self):
        if self.initialized:
            return
        self.setup_glut_environment()
        self.setup_buffers(self.buffer_width, self.buffer_height)
        self.setup_gl_environment()
        self.initialized = True

    def setup_gl_environment(self):
        from OpenGL import GL
        GL.glShadeModel(GL.GL_SMOOTH)
        # glEnable(GL_LIGHTING)
        GL.glDisable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)

        # TODO Call me
        # self.set_camera_perspective(cam_params)

    def setup_glut_environment(self):
        from OpenGL import GLUT
        import sys
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(0, 0)
        self.window_handle = GLUT.glutCreateWindow("Dummy")

    def __del__(self):
        if self.window_handle is not None:
            GLUT.glutDestroyWindow(self.window_handle)

    def render_mesh(self, mesh):
        self.gl_start_triangles()
        for vertices, color in zip(mesh.triangles, mesh.triangle_colors):
            self.gl_color(color)
            for vertex in vertices:
                self.gl_vertex(vertex)
        self.gl_end_triangles()

    def gl_color(self, color):
        GL.glColor3ub(color[0], color[1], color[2])

    def gl_vertex(self, vertex):
        x, y, z = vertex
        GL.glVertex3d(GLdouble(x), GLdouble(y), GLdouble(z))

    def gl_normal(self, normal):
        nx, ny, nz = normal
        GL.glNormal3d(GLdouble(nx), GLdouble(ny), GLdouble(nz))

    def gl_start_triangles(self):
        GL.glBegin(GL.GL_TRIANGLES)

    def gl_end_triangles(self):
        GL.glEnd()

    def gl_start_call_list(self, index):
        list_num = index + 1
        GL.glNewList(GL.GLuint(list_num), GL.GL_COMPILE)

    def gl_end_call_list(self):
        GL.glEndList()

    def add_mesh(self, mesh, index):
        self.create_mesh_call_list(mesh, index)

    def create_mesh_call_list(self, mesh, index):
        self.gl_start_call_list(index)
        self.render_mesh(mesh)
        self.gl_end_call_list()

    def clear_depth(self):
        glClear(GL_DEPTH_BUFFER_BIT)

    def clear_color(self, view_num=None):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def set_modelview_matrix(self, F_camera_world):
        m_column_major = F_camera_world.T.ravel().copy()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(m_column_major)

    def get_modelview_matrix(self):
        # We apply a transpose to the modelview matrix from OpenGL because it is store column major,
        # and Python stores arrays row major
        # This way the matrix has a form [R | T]
        return glGetFloatv(GL_MODELVIEW_MATRIX).T

    def set_frustum(self, l, r, t, b, z_near, z_far):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(l, r, t, b, z_near, z_far)

    def set_camera_perspective(self, cam_params):
        GLCore.set_camera_perspective(self, cam_params)
        fx, fy, cx, cy, w, h = cam_params
        GL.glViewport(0, 0, w, h)

    def render_indices(self, indices):
        self.render_call_lists(indices)

    def render_call_lists(self, indices):
        """ Display function """
        # print self.view_num
        self.clear_color()
        self.clear_depth()
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        for index in indices:
            glCallList(GLuint(index + 1))
        glFlush()

    def setup_buffers(self, w, h):
        if self.framebuffer is not None:
            return
        # Setup framebuffer
        framebuffer = glGenFramebuffersEXT(1)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, framebuffer)

        # Setup depthbuffer
        depthbuffer = glGenRenderbuffersEXT(1)
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, depthbuffer)
        glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT, w, h)
        glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,
                                     GL_DEPTH_ATTACHMENT_EXT,
                                     GL_RENDERBUFFER_EXT, depthbuffer)

        # Setup colorbuffer
        colorbuffer = glGenRenderbuffersEXT(1)
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, colorbuffer)
        glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_RGB, w, h)
        glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,
                                     GL_COLOR_ATTACHMENT0_EXT,
                                     GL_RENDERBUFFER_EXT, colorbuffer)

        # Setup stencilbuffer
        stencilbuffer = None
        # glGenRenderbuffersEXT (1)
        # stencilbuffer = glGenRenderbuffersEXT (1)
        # glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, stencilbuffer);
        # glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT,GL_STENCIL_INDEX, w, h);
        # glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,
        #                              GL_STENCIL_ATTACHMENT_EXT,
        #                              GL_RENDERBUFFER_EXT,
        #                              stencilbuffer);

        self.colorbuffer = colorbuffer
        self.framebuffer = framebuffer
        self.depthbuffer = depthbuffer
        self.stencilbuffer = stencilbuffer
        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        if status != GL_FRAMEBUFFER_COMPLETE_EXT:
            print("Error in framebuffer activation")
        return

    def cleanup_buffers(self):
        # Cleanup, there may be a memory leak here
        colorbuffer = self.colorbuffer
        framebuffer = self.framebuffer
        depthbuffer = self.depthbuffer
        # stencilbuffer = self.stencilbuffer
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, 0)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        if self.framebuffer:
            glDeleteFramebuffersEXT(1, [framebuffer])
        if self.depthbuffer:
            glDeleteRenderbuffersEXT(1, [depthbuffer])
        if self.colorbuffer:
            glDeleteRenderbuffersEXT(1, [colorbuffer])
        # glDeleteRenderbuffersEXT(1, [stencilbuffer])
        self.colorbuffer = None
        self.framebuffer = None
        self.depthbuffer = None
        self.stencilbuffer = None

    def get_projection_matrix(self):
        return glGetDoublev(GL_PROJECTION_MATRIX).T

    def data(self, color=True, depth=True, xyz_camera=False, xyz_world=False, use_byte=False):
        """ Offscreen rendering
        Save an offscreen rendering of size (w,h) to filename.
        """
        # print "Getting data"
        RGB = D = XYZ_camera = XYZ_world = None
        depthType = GL_UNSIGNED_BYTE if use_byte else GL_FLOAT
        x0, y0, w, h = 0, 0, self.width, self.height
        if color:
            color_data = glReadPixels(x0, y0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
            RGB = np.resize(np.fromstring(color_data, dtype=np.uint8), [h, w, 3])
        if depth or xyz_world or xyz_camera:
            depth_data = glReadPixels(x0, y0, w, h, GL_DEPTH_COMPONENT, depthType)
            XYZ_camera, XYZ_world = unproject(self, depth_data, xyz_camera=xyz_camera, xyz_world=xyz_world)
        if depth:
            D = np.resize(depth_data, [h, w])
        return self.RenderedImages(RGB, D, XYZ_camera, XYZ_world)

    def get_viewport(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        viewport = np.array(viewport)
        return viewport

    def get_frame_opengl_world(self):
        F_opengl_world = glGetDoublev(GL_MODELVIEW_MATRIX).T
        return F_opengl_world
