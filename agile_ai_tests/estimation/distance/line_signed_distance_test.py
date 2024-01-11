import numpy as np

from agile_ai.estimation.distance.line_signed_distance import LineSignedDistance
from agile_ai.geometry.pose_conversions import normed
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import close_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


@pyne
def line_signed_distance_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#compute_distance")
    def _():
        @it("returns the signed distance")
        def _(tc: TestContext):
            vector = np.array([3.0, 5.0])
            normal = normed(vector)
            point = np.array([6.0, 10.0])
            lsd = LineSignedDistance(point, vector)
            points = np.array([point + normal * -1.35,
                               point,
                               point + normal * +3.25
                               ]).T
            distances = lsd.compute_distance(points)
            expect(distances).to_be(close_to_array(np.array([-1.35, 0.0, 3.25])))

        @describe("when the line width is set")
        def _():
            @it("returns the signed distance starting from half width from the center line")
            def _(tc: TestContext):
                vector = np.array([3.0, 5.0])
                normal = normed(vector)
                point = np.array([6.0, 10.0])
                lsd = LineSignedDistance(point, vector, width=3.0)
                points = np.array([
                                   point + normal * -1.55,
                                   point + normal * -1.35,
                                   point,
                                   point + normal * +1.25,
                                   point + normal * +3.55
                                   ]).T
                distances = lsd.compute_distance(points)
                expect(distances).to_be(close_to_array(np.array([-0.05, 0.0, 0.0, 0.0, 2.05])))

