from agile_ai.data_marshalling.numeric_types import Float2, FloatN2, FloatN
from agile_ai.geometry.pose_conversions import normed


class LineSignedDistance:
    point: Float2
    normal: Float2
    center_distance: float
    half_width: float

    def __init__(self, point: Float2, normal: Float2, width=0.0):
        self.point = point
        self.normal = normed(normal)
        self.center_distance = self.point @ self.normal
        self.half_width = width / 2.0

    def compute_distance(self, points: FloatN2) -> FloatN:
        dot_product = self.normal @ points
        if self.half_width:
            line_distance = dot_product - self.center_distance
            min_distance = line_distance + self.half_width
            max_distance = line_distance - self.half_width
            use_zero = abs(line_distance) < self.half_width
            abs_min_distance = abs(min_distance)
            abs_max_distance = abs(max_distance)
            use_max = abs_max_distance < abs_min_distance
            distance = min_distance
            distance[use_max] = max_distance[use_max]
            distance[use_zero] = 0
            return distance
        else:
            return dot_product - self.center_distance
