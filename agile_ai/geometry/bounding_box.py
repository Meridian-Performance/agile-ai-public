import numpy as np


class BoundingBox:
    def __init__(self, x_min, y_min, z_min, x_max, y_max, z_max):
        self.x_min = x_min
        self.y_min = y_min
        self.z_min = z_min
        self.x_max = x_max
        self.y_max = y_max
        self.z_max = z_max
        if not np.all(self.x_min <= self.x_max):
            raise ValueError("x_min > x_max: (x_min: %s, x_max: %s)" % (x_min, x_max))
        if not np.all(self.y_min <= self.y_max):
            raise ValueError("y_min > y_max: (y_min: %s, y_max: %s)" % (y_min, y_max))
        if not np.all(self.z_min <= self.z_max):
            raise ValueError("z_min > z_max: (z_min: %s, z_max: %s)" % (z_min, z_max))

    @property
    def center(self):
        return np.array([(self.x_max + self.x_min) / 2.0, (self.y_max + self.y_min) / 2.0, (self.z_max + self.z_min) / 2.0])

    @property
    def volume(self):
        x_width, y_width, z_width = self.widths
        volume = x_width
        volume *= y_width
        volume *= z_width
        return volume

    @property
    def widths(self):
        x_width = self.x_max - self.x_min
        y_width = self.y_max - self.y_min
        z_width = self.z_max - self.z_min
        return x_width, y_width, z_width

    @property
    def min_point(self):
        return (self.x_min, self.y_min, self.z_min)

    @property
    def max_point(self):
        return (self.x_max, self.y_max, self.z_max)

    @property
    def mid_point(self):
        return (np.array(self.max_point) + np.array(self.min_point))/2.0

    @property
    def bounds_values(self):
        return (self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max)

    @property
    def min_max_point_pair(self):
        return (self.x_min, self.y_min, self.z_min), (self.x_max, self.y_max, self.z_max)

    @property
    def per_axis_min_max_pairs(self):
        return (self.x_min, self.x_max), (self.y_min, self.y_max), (self.z_min, self.z_max)

    @property
    def has_volume(self):
        return (self.x_max > self.x_min) and (self.y_max > self.y_min) and (self.z_max > self.z_min)

    def contains_point(self, point, margin=0):
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = self.per_axis_min_max_pairs
        min_x -= margin
        max_y += margin
        min_y -= margin
        max_x += margin
        min_z -= margin
        max_z += margin
        x, y, z = point
        contains_x = np.logical_and(min_x <= x, x <= max_x)
        contains_y = np.logical_and(min_y <= y, y <= max_y)
        contains_z = np.logical_and(min_z <= z, z <= max_z)
        contains = contains_x
        contains &= contains_y
        contains &= contains_z
        return contains

    def _intersect(self, other):
        box_a = self
        box_b = other
        (amin_x, amax_x), (amin_y, amax_y), (amin_z, amax_z) = box_a.per_axis_min_max_pairs
        (bmin_x, bmax_x), (bmin_y, bmax_y), (bmin_z, bmax_z) = box_b.per_axis_min_max_pairs
        cmin_x = np.maximum(amin_x, bmin_x)
        cmax_x = np.minimum(amax_x, bmax_x)
        cmin_y = np.maximum(amin_y, bmin_y)
        cmax_y = np.minimum(amax_y, bmax_y)
        cmin_z = np.maximum(amin_z, bmin_z)
        cmax_z = np.minimum(amax_z, bmax_z)

        overlap_x = (cmax_x - cmin_x) > 0
        overlap_y = (cmax_y - cmin_y) > 0
        overlap_z = (cmax_z - cmin_z) > 0
        overlap = overlap_x
        overlap &= overlap_y
        overlap &= overlap_z
        return cmin_x, cmin_y, cmin_z, cmax_x, cmax_y, cmax_z, overlap

    def intersect(self, other):
        cmin_x, cmin_y, cmin_z, cmax_x, cmax_y, cmax_z, overlap = self._intersect(other)
        if not overlap:
            return BoundingBox(0, 0, 0, 0, 0, 0)
        return BoundingBox(cmin_x, cmin_y, cmin_z, cmax_x, cmax_y, cmax_z)

    def expand_by_half_width(self, half_width):
        box = self.copy()
        box.x_min -= half_width
        box.x_max += half_width
        box.y_min -= half_width
        box.y_max += half_width
        box.z_min -= half_width
        box.z_max += half_width
        return box

    def expand_by_factor(self, factor):
        box = self.copy()
        box.x_min *= factor
        box.x_max *= factor
        box.y_min *= factor
        box.y_max *= factor
        box.z_min *= factor
        box.z_max *= factor
        return box

    def translate(self, translation):
        box = self.copy()
        tx, ty, tz = translation
        box.x_min += tx
        box.x_max += tx
        box.y_min += ty
        box.y_max += ty
        box.z_min += tz
        box.z_max += tz
        return box

    @staticmethod
    def check_intersection(min_max_values_a, min_max_values_b, margin=0, inclusive=False):
        (amin_x, amin_y, amin_z, amax_x, amax_y, amax_z) = min_max_values_a
        (bmin_x, bmin_y, bmin_z, bmax_x, bmax_y, bmax_z) = min_max_values_b
        cmin_x = np.maximum(amin_x, bmin_x)
        cmax_x = np.minimum(amax_x, bmax_x)
        cmin_y = np.maximum(amin_y, bmin_y)
        cmax_y = np.minimum(amax_y, bmax_y)
        cmin_z = np.maximum(amin_z, bmin_z)
        cmax_z = np.minimum(amax_z, bmax_z)
        delta_x = (cmax_x - cmin_x)
        delta_y = (cmax_y - cmin_y)
        delta_z = (cmax_z - cmin_z)
        if inclusive:
            overlap_x = delta_x >= -margin
            overlap_y = delta_y >= -margin
            overlap_z = delta_z >= -margin
        else:
            overlap_x = delta_x > -margin
            overlap_y = delta_y > -margin
            overlap_z = delta_z > -margin
        overlap = overlap_x.copy()
        overlap &= overlap_y
        overlap &= overlap_z
        return overlap


