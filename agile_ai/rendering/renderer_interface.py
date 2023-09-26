
class RendererInterface:
    def clear_color(self):
        pass

    def render(self):
        raise NotImplementedError

    def get_data(self, color=True, depth=False):
        raise NotImplementedError

