from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.utilities.option import Option
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
    empty_option: Option
    present_option: Option
    none_present_option: Option


@pyne
def option_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.empty_option = Option.empty()
        tc.present_option = Option(0)
        tc.none_present_option = Option(None)

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

        @describe("when it is an present option with a None value")
        def _():
            @it("returns True")
            def _(tc: TestContext):
                expect(tc.none_present_option.is_present()).to_be(True)

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

        @describe("when it is an present option with a None value")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.none_present_option.is_empty()).to_be(False)

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

        @describe("when it is an present option with a None value")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.none_present_option.get()).to_be(None)
