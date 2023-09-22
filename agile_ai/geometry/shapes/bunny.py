"""Load the standford bunny mesh."""
from agile_ai.geometry.mesh import Mesh
from agile_ai.resources import resources_directory


class Bunny(Mesh):
    """Standford bunny class."""

    # pylint: disable=super-init-not-called
    def __init__(self, use_orig=False):
        """Copy the dict of the bunny mesh."""
        mesh = (resources_directory / "bunny.obj").get()
        self.__dict__ = mesh.__dict__
        if not use_orig:
            import numpy as np
            self.rotate_x(np.pi / 2.0)
            self.scale(20)
            self.center_midpoints()
            self.translate_to_xy_plane()
