import numpy as np

from agile_ai.data_marshalling.numeric_types import Int2D
from agile_ai.estimation.attention_estimator import AttentionEstimator
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub

VISUALIZE = False


class TestContext(TCBase):
    __services__: Marker
    attention_estimator: AttentionEstimator

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    image: Int2D


def get_energy_image():
    image = (resources_directory / "png" // "energy.png").get()
    return image


@pyne
def attention_estimator_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.image = get_energy_image()


    @describe("#sum_filter")
    def _():
        @it("returns the sum filter of the mask by the window size")
        def _(tc: TestContext):
            mask = np.zeros((100, 100), dtype=bool)
            mask[(48, 49, 50, 51, 52), (48, 49, 50, 51, 52)] = True
            center_sum = tc.attention_estimator.sum_filter(mask, 2)
            expect(center_sum[45, 45]).to_be(0)
            expect(center_sum[46, 46]).to_be(1)
            expect(center_sum[47, 47]).to_be(2)
            expect(center_sum[48, 48]).to_be(3)
            expect(center_sum[49, 49]).to_be(4)
            expect(center_sum[50, 50]).to_be(5)
            expect(center_sum[51, 51]).to_be(4)
            expect(center_sum[52, 52]).to_be(3)
            expect(center_sum[53, 53]).to_be(2)
            expect(center_sum[54, 54]).to_be(1)
            expect(center_sum[55, 55]).to_be(0)

            if VISUALIZE:
                import pylab
                pylab.imshow(center_sum)
                pylab.show()

    @describe("#estimate_regions")
    def _():
        @it("returns regions of interest")
        def _(tc: TestContext):
            mask = tc.image > 0
            centers = tc.attention_estimator.estimate_centers(mask, 30, 30, 1000)
            expected_peak = (600, 300)
            if VISUALIZE:
                sum_image = tc.attention_estimator.sum_filter(mask, 30)
                import pylab
                pylab.subplot(2, 1, 1)
                pylab.imshow(mask)
                pylab.scatter(*centers.T, color='c')
                pylab.subplot(2, 1, 2)
                pylab.imshow(sum_image)
                pylab.scatter(*centers.T, color='c')
                pylab.show()
            distances = np.linalg.norm(expected_peak - centers, axis=1)
            min_distance = distances.min()
            expect(min_distance).to_be_between(0, 15)
