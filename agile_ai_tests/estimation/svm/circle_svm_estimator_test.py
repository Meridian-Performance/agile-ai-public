import numpy as np

from agile_ai.estimation.svm.circle_svm_estimator import CircleSvmEstimator
from agile_ai.estimation.svm.embedded_svm_estimator import SvmExemplars
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import close_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    circle_svm_estimator: CircleSvmEstimator

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    exemplars_2D: SvmExemplars

VISUALIZE = False


def get_circle_points() -> SvmExemplars:
    random_state = np.random.RandomState(0)
    X = random_state.random((1000, 2))
    R = np.sqrt(((X - (.4, .5)) ** 2).sum(1))
    mask = (R < .3)
    return SvmExemplars.from_points_and_mask(X, mask)



@pyne
def circle_svm_estimator_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#embed_exemplars")
    def _():
        @it("remaps")
        def _(tc: TestContext):
            theta = np.linspace(0, 2*np.pi, 100)
            X = np.sin(theta)
            Y = np.cos(theta)
            XY = np.array((X, Y)).T
            points = np.vstack([0.1 * XY, 0.2 * XY, 0.3 * XY, 0.4 * XY, 0.5 * XY]) + (0.5, 0.2)
            R = np.linalg.norm(points - (0.5, 0.2), axis=1)
            exemplars_2D = SvmExemplars.from_points_and_mask(points, np.ones(len(points), dtype=bool))
            tc.circle_svm_estimator.set_exemplars(exemplars_2D)
            tc.circle_svm_estimator.embed_exemplars(0.5, 0.2)
            if VISUALIZE:
                tc.circle_svm_estimator.visualize_exemplars_ND()
            expect(tc.circle_svm_estimator.exemplars_ND.X.T[2]).to_be(close_to_array(R))

    @describe("#fit")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.exemplars_2D = get_circle_points()
            tc.circle_svm_estimator.set_exemplars(tc.exemplars_2D)
            tc.circle_svm_estimator.embed_exemplars(0.3, 0.4)

        @it("predicts most of the circle points")
        def _(tc: TestContext):
            tc.circle_svm_estimator.fit()
            if VISUALIZE:
                tc.exemplars_2D.visualize()
                tc.circle_svm_estimator.visualize_exemplars_2D()
                tc.circle_svm_estimator.visualize_exemplars_ND()
                tc.circle_svm_estimator.visualize_predictions_ND()
            correct_count = (tc.circle_svm_estimator.exemplars_2D.y == tc.circle_svm_estimator.predictions_ND.y).sum()
            expect(correct_count).to_be_between(950, 1000)

        @it("estimates the circle center and radius from the plane parameters")
        def _(tc: TestContext):
            tc.circle_svm_estimator.fit()
            tc.circle_svm_estimator.reembed_exemplars()
            tc.circle_svm_estimator.fit()
            if VISUALIZE:
                # tc.circle_svm_estimator.visualize_decision_surface_ND()
                tc.circle_svm_estimator.visualize_decision_surface_2D()
            print(tc.circle_svm_estimator.intercept, tc.circle_svm_estimator.normal)
