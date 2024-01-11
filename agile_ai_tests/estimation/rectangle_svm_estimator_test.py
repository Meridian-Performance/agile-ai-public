import numpy as np
from agile_ai.estimation.embedded_svm_estimator import SvmExemplars
from agile_ai.estimation.rectangle_svm_estimator import RectangleSvmEstimator

from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, TCBase, xit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub

VISUALIZE = True


class TestContext(TCBase):
    __services__: Marker
    rectangle_svm_estimator: RectangleSvmEstimator
    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


def get_rectangle_points() -> SvmExemplars:
    random_state = np.random.RandomState(0)
    X = random_state.random((500, 2))
    mask = (X[:, 0] > .2) * (X[:, 0] < .5)
    return SvmExemplars.from_points_and_mask(X, mask)


@pyne
def rectangle_svm_estimator_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#estimate")
    def _():
        @describe("#estimate")
        def _():
            @xit("estimates the bounding lines of the rectangle")
            def _(tc: TestContext):
                exemplars_2D = get_rectangle_points()
                tc.rectangle_svm_estimator.set_exemplars(exemplars_2D)
                tc.rectangle_svm_estimator.embed_exemplars(0.4)
                tc.rectangle_svm_estimator.fit()
                if VISUALIZE:
                    exemplars_2D.visualize()
                    tc.rectangle_svm_estimator.visualize_exemplars_2D()
                    tc.rectangle_svm_estimator.visualize_exemplars_ND()
                    tc.rectangle_svm_estimator.visualize_predictions_ND()
                # print((y_pred == exemplars_2D.y).sum(), len(exemplars_2D.y))

