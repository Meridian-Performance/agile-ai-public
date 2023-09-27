from agile_ai.injection.decorators import autowire
from agile_ai.rendering.gl_renderer import GLRenderer
from agile_ai.rendering.moderngl_core import ModernGLCore


class ModernGLRenderer(GLRenderer):
    core: ModernGLCore = autowire(ModernGLCore)
