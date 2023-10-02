from typing import Tuple

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

from agile_ai.drawing.canvas import FixedCanvas


class OffscreenCanvas(FixedCanvas):
    shape: Tuple[int, int]

    def __init__(self, shape, h_inches=4.0, **kwargs):
        h_px, w_px = shape
        FixedCanvas.__init__(self, w_px, h_px, h_inches, **kwargs)
        self.shape = shape

    def gca(self):
        return self.ax

    def gcf(self):
        return self.fig

    def create_figure(self):
        fig = Figure(figsize=(self.w_inches, self.h_inches), dpi=self.dpi, facecolor='k')
        self.canvas = FigureCanvasAgg(fig)
        return fig

    def create_axis(self, vmin, vmax, adjs=None):
        return [vmin, vmin, vmax, vmax]

    def get_array(self, alpha=False):
        self.ax.axis([0, self.w_px, self.h_px, 0])
        return get_array(self, alpha)


def get_array(fig, alpha=False):
    fig.canvas.draw()
    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (h, w, 4)

    # drawing.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    x = 4 if alpha else 3
    data = np.roll(buf, 3, axis=2)[..., :x]
    return data
