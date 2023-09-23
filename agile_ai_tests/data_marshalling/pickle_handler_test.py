from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


@pyne
def pickle_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
