import cv2
import numpy as np

from agile_ai.data_marshalling.numeric_types import Bool2D, Int2D
from agile_ai.injection.interfaces import Service


class AttentionEstimator(Service):
    def sum_filter(self, mask: Bool2D, window_half_width: int) -> Int2D:
        window_width = 2 * window_half_width + 1
        integral_image = cv2.integral(mask.astype(np.uint8))
        center_sum = np.zeros_like(mask, dtype=int)
        min_slc = slice(None, -window_width)
        max_slc = slice(window_width, None)
        cnt_slc = slice(window_half_width, -window_half_width)
        bottom_right = integral_image[min_slc, min_slc]
        top_left = integral_image[max_slc, max_slc]
        top_right = integral_image[max_slc, min_slc]
        bottom_left = integral_image[min_slc, max_slc]
        center_sum[cnt_slc, cnt_slc] = bottom_right + top_left - top_right - bottom_left
        return center_sum

    def estimate_centers(self, mask: Bool2D, patch_size: int, suppression_size: int, min_energy: int):
        sum_image = self.sum_filter(mask, patch_size)
        return self.extract_peaks(sum_image, suppression_size, min_energy)

    def extract_peaks(self, energy_image, suppression_size: int, min_energy: int, max_peak_count: int = np.inf):
        energy_image[energy_image < min_energy] = 0
        R, C = energy_image.nonzero()
        V  = energy_image[R, C]
        asort = V.argsort()[::-1]
        V = V[asort]
        R = R[asort]
        C = C[asort]
        centers = []
        for v, r, c in zip(V, R, C):
            if not energy_image[r, c]:
                continue
            centers.append((c, r))
            if len(centers) > max_peak_count:
                break
            slc = slice(max(0, r-suppression_size), r+suppression_size+1), slice(max(0, c-suppression_size), c+suppression_size+1)
            energy_image[slc] = 0
        return np.array(centers)
