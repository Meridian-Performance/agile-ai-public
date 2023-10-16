from pathlib import Path

from agile_ai.data_marshalling.txt_handler import TxtHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import TCBase, before_each, describe, it
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    txt_path: Path


@pyne
def txt_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.txt_path = tc.test_directory.path / "file.txt"

    @describe("#load")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            with tc.txt_path.open("w") as fh:
                fh.write("some text string\nsome other line\n")
            text = TxtHandler.load(tc.txt_path)
            expect(text).to_be("some text string\nsome other line\n")

    @describe("#save")
    def _():
        @it("saves the string to file")
        def _(tc: TestContext):
            TxtHandler.save(tc.txt_path, "some text string\nsome other line\n")
            with tc.txt_path.open("r") as fh:
                text = fh.read()
            expect(tc.txt_path).to_be(an_existing_path())
            expect(text).to_be("some text string\nsome other line\n")

    @describe("#matches")
    def _():
        @it("matches only .obj extensions")
        def _(tc: TestContext):
            expect(TxtHandler.matches("test.txt")).to_be(True)
            expect(TxtHandler.matches("test.txt_")).to_be(False)
    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.txt")._handler).to_be(TxtHandler)
