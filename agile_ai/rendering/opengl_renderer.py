from .gl_renderer import GLRenderer
from .opengl_core import OpenGLCore


class OpenGLRenderer(GLRenderer):
    pass


OpenGLRenderer.GLCore = OpenGLCore
