from agile_ai.injection.decorators import Marker
from agile_ai.utilities.memo_option import MemoOption
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.spy import Spy
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    spy: Spy
    empty_option: MemoOption
    present_option: MemoOption


@pyne
def memo_option_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.empty_option = MemoOption.empty()
        tc.spy = Spy()
        tc.spy.then_return(0)
        tc.present_option = MemoOption(tc.spy)

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
            @describe("when it is called for the first time")
            def _():
                @it("returns the result of the function")
                def _(tc: TestContext):
                    expect(tc.present_option.get()).to_be(0)
                    expect(tc.spy).was_called()

            @describe("when it is called for the second time")
            def _():
                @it("returns the result of the function, only calling it once")
                def _(tc: TestContext):
                    expect(tc.present_option.get()).to_be(0)
                    expect(tc.present_option.get()).to_be(0)
                    expect(tc.spy.calls).to_have_length(1)
