import pickle
from pathlib import Path

from agile_ai.data_marshalling.pkl_handler import PklHandler
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
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
    path: Path

@pyne
def pkl_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.path = tc.test_directory.path / "file.pkl"

    @describe("#load")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            with tc.path.open("wb") as file:
                pickle.dump(dict(a="c", b=1), file)
            content = PklHandler.load(tc.path)
            expect(content).to_be(dict(a="c", b=1))

    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            PklHandler.save(tc.path, dict(a="c", b="1"))
            with tc.path.open("rb") as file:
                content = pickle.load(file)
            expect(tc.path).to_be(an_existing_path())
            expect(content).to_be(dict(a="c", b="1"))

    @describe("#matches")
    def _():
        @it("matches only .pkl extensions")
        def _(tc: TestContext):
            expect(PklHandler.matches("test.pkl")).to_be(True)
            expect(PklHandler.matches("test.pkl_")).to_be(False)
    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.pkl")._handler).to_be(PklHandler)
