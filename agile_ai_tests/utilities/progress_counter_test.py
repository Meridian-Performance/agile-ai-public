from agile_ai.injection.decorators import autowire_services, Marker, get_service
from agile_ai.utilities.progress_counter import ProgressCounter
from agile_ai.utilities.time_provider import TimeProvider
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, with_stubs
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.attached_spy import AttachedSpy, attach_stub
from pynetest.test_doubles.spy import Spy
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    time_provider: TimeProvider

    __stubs__: Marker
    stubs: MegaStub
    now_spy: AttachedSpy
    print_spy: AttachedSpy

    __other__: Marker
    progress_counter: ProgressCounter


@pyne
def progress_counter_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.now_spy = attach_stub(tc.time_provider, "now")
        tc.stubs = tc.now_spy

    @describe("__call__")
    def _():
        @describe("when min_sec_delta is set to non-none value")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.progress_counter = ProgressCounter(min_sec_delta=1.0)
                tc.print_spy = attach_stub(tc.progress_counter, "print_msg")
                tc.stubs = MegaStub(tc.now_spy, tc.print_spy)

            @describe("when subsequent calls are within min_sec_delta")
            def _():
                @before_each
                def _(tc: TestContext):
                    tc.now_spy.then_return_sequence([0.1, 0.2, 0.4])

                @it("only prints the first call")
                @with_stubs
                def _(tc: TestContext):
                    tc.progress_counter("message 1")
                    tc.progress_counter("message 2")
                    tc.progress_counter("message 3")
                    expect(tc.print_spy.calls).to_have_length(1)

            @describe("when subsequent calls are outside min_sec_delta")
            def _():
                @before_each
                def _(tc: TestContext):
                    tc.now_spy.then_return_sequence([0.0, 0.5, 1.0001, 2.0002])

                @it("prints all calls")
                @with_stubs
                def _(tc: TestContext):
                    tc.progress_counter("message 1")
                    tc.progress_counter("message 2")
                    tc.progress_counter("message 3")
                    tc.progress_counter("message 4")
                    expect(tc.print_spy.calls).to_have_length(3)

        @describe("when min_sec_delta is set to none value")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.progress_counter = ProgressCounter(min_sec_delta=None)
                tc.print_spy = attach_stub(tc.progress_counter, "print_msg")
                tc.stubs = MegaStub(tc.print_spy)

            @it("only prints all calls")
            @with_stubs
            def _(tc: TestContext):
                tc.progress_counter("message 1")
                tc.progress_counter("message 2")
                tc.progress_counter("message 3")
                expect(tc.print_spy.calls).to_have_length(3)

    @describe("when the max_count is not specified")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.progress_counter = ProgressCounter(min_sec_delta=None, max_count=None, label="Progress test")
            tc.print_spy = attach_stub(tc.progress_counter, "print_msg")
            tc.stubs = tc.print_spy

        @it("includes the count in completion information in the printed message")
        @with_stubs
        def _(tc: TestContext):
            tc.progress_counter("test 1")
            tc.progress_counter("test 2")
            tc.progress_counter("test 7", step=5)
            tc.progress_counter("test 8")
            tc.progress_counter("test 9")
            tc.progress_counter("test 10")
            expect(tc.print_spy.calls).to_have_length(6)
            expect(tc.print_spy.calls[0].args[0]).to_be("Progress test [1/??]: test 1")
            expect(tc.print_spy.calls[1].args[0]).to_be("Progress test [2/??]: test 2")
            expect(tc.print_spy.calls[2].args[0]).to_be("Progress test [7/??]: test 7")
            expect(tc.print_spy.calls[3].args[0]).to_be("Progress test [8/??]: test 8")
            expect(tc.print_spy.calls[4].args[0]).to_be("Progress test [9/??]: test 9")
            expect(tc.print_spy.calls[5].args[0]).to_be("Progress test [10/??]: test 10")

    @describe("when the max_count is specified")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.progress_counter = ProgressCounter(min_sec_delta=None, max_count=10, label="Progress test")
            tc.print_spy = attach_stub(tc.progress_counter, "print_msg")
            tc.stubs = tc.print_spy

        @it("includes the percentage in completion information in the printed message")
        @with_stubs
        def _(tc: TestContext):
            tc.progress_counter("test 1")
            tc.progress_counter("test 2")
            tc.progress_counter("test 7", step=5)
            tc.progress_counter("test 8")
            tc.progress_counter("test 9")
            tc.progress_counter("test 10")
            expect(tc.print_spy.calls).to_have_length(6)
            expect(tc.print_spy.calls[0].args[0]).to_be("Progress test [1/10] (10.0%): test 1")
            expect(tc.print_spy.calls[1].args[0]).to_be("Progress test [2/10] (20.0%): test 2")
            expect(tc.print_spy.calls[2].args[0]).to_be("Progress test [7/10] (70.0%): test 7")
            expect(tc.print_spy.calls[3].args[0]).to_be("Progress test [8/10] (80.0%): test 8")
            expect(tc.print_spy.calls[4].args[0]).to_be("Progress test [9/10] (90.0%): test 9")
            expect(tc.print_spy.calls[5].args[0]).to_be("Progress test [10/10] (100.0%): test 10")
