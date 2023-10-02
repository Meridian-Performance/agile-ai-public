import pylab


class Canvas:
    def __init__(self, vmin=0, vmax=1, adjs=None):
        self.fig = self.create_figure()
        self.ax = self.create_axis(vmin, vmax, adjs=adjs)
        self.ax = self.fig.add_axes(self.ax)
        self.set_axes_visible(False)
        export = ["cla", "arrow", "text"]
        for name in export:
            setattr(self, name, getattr(pylab, name))
        # self.draw()

    def axis(self, *args):
        return self.gca().axis(*args)

    def draw(self):
        self.gcf().canvas.draw()

    def add_patch(self, patch):
        self.gca().add_patch(patch)

    def create_axis(self, vmin, vmax, adjs=None):
        if adjs is None:
            adjs = [vmin, vmin, vmax, vmax]
        return pylab.Axes(self.fig, adjs)

    def create_figure(self):
        return pylab.figure()

    def set_axes_visible(self, visible):
        axis = self.get_axis()
        axis.spines['bottom'].set_visible(visible)
        axis.spines['left'].set_visible(visible)
        axis.spines['top'].set_visible(visible)
        axis.spines['right'].set_visible(visible)
        axis.xaxis.set_visible(visible)
        axis.yaxis.set_visible(visible)

    def get_ratio_h_over_w(self):
        fig = self.get_figure()
        return float(fig.get_figheight()) / float(fig.get_figwidth())

    def set_view_hw(self, cx, cy, hwx, flip_y=False):
        hwy = self.get_ratio_h_over_w() * hwx
        axis = (cx - hwx, cx + hwx, cy - hwy, cy + hwy) if flip_y else (cx - hwx, cx + hwx, cy + hwy, cy - hwy)
        self.set_axis(axis)

    def set_view(self, cx, cy, hwx, flip_y=False):
        hwy = self.get_ratio_h_over_w() * hwx
        axis = (cx - hwx, cx + hwx, cy - hwy, cy + hwy) if flip_y else (cx - hwx, cx + hwx, cy + hwy, cy - hwy)
        self.set_axis(axis)

    def set_axis(self, axis):
        self.get_axis().axis(axis)
        pylab.draw()

    def clear(self):
        lists = []
        lists.append(self.ax.lines)
        lists.append(self.ax.images)
        lists.append(self.ax.patches)
        lists.append(self.ax.collections)
        lists.append(self.ax.artists)
        lists.append(self.ax.texts)
        for l in lists:
            while len(l) > 0:
                l[0].remove()

    def get_figure(self):
        return self.fig

    def get_axis(self):
        return self.ax

    def imshow(self, img, **kwargs):
        ret = self.get_axis().imshow(img, **kwargs)
        pylab.draw()
        return ret

    def plot(self, x, y, **kwargs):
        ret = self.get_axis().plot(x, y, **kwargs)
        self.draw()
        return ret

    def scatter(self, x, y, **kwargs):
        ret = self.get_axis().scatter(x, y, **kwargs)
        self.draw()
        return ret

    def draw(self):
        self.gcf().canvas.draw()


class PylabCanvas(Canvas):
    def __init__(self):
        for attr in dir(pylab):
            setattr(self, attr, getattr(pylab, attr))
        # export = ["cla","clf","scatter","plot","imshow","draw","axis",'gca']
        # for name in export:
        #  setattr(self,name,getattr(pylab,name))

    def get_figure(self):
        return pylab.gcf()

    def get_axis(self):
        return pylab.gca()

    def add_patch(self, patch):
        pylab.gca().add_patch(patch)

    def set_view(self, cx, cy, hwx):
        pass


class CurrentCanvas(Canvas):
    def __init__(self):
        Canvas.__init__(self)
        for attr in dir(pylab):
            setattr(self, attr, getattr(pylab, attr))

    def create_axis(self, *args):
        pylab.clf()
        return pylab.Axes(self.fig, [0, 0, 1, 1])

    def create_figure(self):
        return pylab.gcf()

    def get_figure(self):
        return pylab.gcf()

    def get_axis(self):
        return pylab.gca()


class FixedCanvas(Canvas):
    def __init__(self, w_px, h_px, h_inches=4.0, **kwargs):
        self.ratio_w_over_h = w_px / float(h_px)
        self.ratio_h_over_w = 1.0 / self.ratio_w_over_h
        self.w_inches = self.ratio_w_over_h * h_inches
        self.h_inches = h_inches
        self.dpi = h_px / float(h_inches)
        self.shape = (h_px, w_px)
        self.w_px = w_px
        self.h_px = h_px
        Canvas.__init__(self, **kwargs)

    def set_dpi(self, dpi):
        self.dpi = dpi

    def savefig(self, fn, **kwargs):
        pylab.savefig(fn, dpi=self.dpi, **kwargs)

    def gcf(self):
        return self.fig

    def gca(self):
        return self.ax

    def get_ratio_h_over_w(self):
        return self.ratio_h_over_w

    def set_view(self, x1, y1, width):
        height = self.get_ratio_h_over_w() * width
        self.axis((x1, x1 + width, y1 + height, y1))

    def create_figure(self):
        fig = pylab.figure(figsize=(self.w_inches, self.h_inches), dpi=self.dpi)
        return fig


cc = None


def get_current_canvas():
    global cc
    if cc == None:
        cc = CurrentCanvas()
    return cc
# cc = Pylab()
