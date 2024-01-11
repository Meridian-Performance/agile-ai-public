from agile_ai.data_marshalling.numeric_types import Float2, FloatN2, FloatN
from agile_ai.geometry.pose_conversions import normed


class BeamSignedDistance:
    point: Float2
    normal: Float2
    center_distance: float
    half_width: float

    def __init__(self, point: Float2, normal: Float2, width: float):
        self.point = point
        self.normal = normed(normal)
        self.center_distance = self.point @ self.normal
        self.half_width = width / 2.0

    def compute_distance(self, points: FloatN2) -> FloatN:
        # | | |
        # | | |
        # a b c
        # | | |
        # | | |

        dot_product = self.normal @ points
        b_distance = dot_product - self.center_distance
        a_distance = +b_distance - self.half_width
        c_distance = -b_distance - self.half_width
        distance = c_distance.copy()
        use_a = abs(a_distance) < abs(c_distance)
        distance[use_a] = a_distance[use_a]
        return distance
