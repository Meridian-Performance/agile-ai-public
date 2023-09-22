from agile_ai.geometry.mesh_builder import MeshBuilder


class Cube(MeshBuilder):
    """Origin centered cube."""

    def __init__(self, **kwargs):
        """Create the cube."""
        MeshBuilder.__init__(self)
        self.create_side("XYpZ", kwargs)
        self.create_side("XYnZ", kwargs)
        self.create_side("XZpY", kwargs)
        self.create_side("XZnY", kwargs)
        self.create_side("YZpX", kwargs)
        self.create_side("YZnX", kwargs)
        self.build()

    def create_side(self, ABsC, disable):
        """Create the side encoded by ABsC."""
        do_side = disable.get(ABsC, True)
        if not do_side:
            return
        A, B, s, C = ABsC
        Pa = [+1, +1, -1, -1]
        Pb = [+1, -1, -1, +1]
        c = 1
        if s == 'n':
            c = -1
        else:
            Pa = Pa[::-1]
            Pb = Pb[::-1]
        if C == "Y":
            Pa = Pa[::-1]
            Pb = Pb[::-1]

        Pc = [c, c, c, c]
        Ps = []
        Ps.append((A, Pa))
        Ps.append((B, Pb))
        Ps.append((C, Pc))
        _, Ps = zip(*sorted(Ps))
        Vs = zip(*Ps)
        self.add_quad_v(*Vs)
