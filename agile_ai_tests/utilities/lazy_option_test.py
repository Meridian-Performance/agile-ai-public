from agile_ai.injection.decorators import Marker
from agile_ai.utilities.lazy_option import LazyOption
from agile_ai.utilities.option import Option
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
    empty_option: LazyOption
    present_option: LazyOption


@pyne
def lazy_option_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.empty_option = LazyOption.empty()
        tc.present_option = LazyOption(lambda: 0)

    @describe("#is_present")
    def _():
        @describe("when it is an empty option")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.empty_option.is_present()).to_be(False)

        @describe("when it is an present option")
        def _():
            @it("returns True")
            def _(tc: TestContext):
                expect(tc.present_option.is_present()).to_be(True)
    @describe("#is_empty")
    def _():
        @describe("when it is an empty option")
        def _():
            @it("returns True")
            def _(tc: TestContext):
                expect(tc.empty_option.is_empty()).to_be(True)

        @describe("when it is an present option")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.present_option.is_empty()).to_be(False)

    @describe("#get")
    def _():
        @describe("when it is an empty option")
        def _():
            @it("raises as Exception")
            def _(tc: TestContext):
                expect(tc.empty_option.get).to_raise_error_of_type(ValueError)

        @describe("when it is an present option")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.present_option.get()).to_be(0)