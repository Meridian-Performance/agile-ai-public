from pathlib import Path

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.data_marshalling.txt_handler import TxtHandler
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit, fdescribe
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
def file_path_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#__init__")
    def _():
        @describe("when created with a Path")
        def _():
            @it("it sets the path")
            def _(tc: TestContext):
                file_path = FilePath(Path("/tmp/some_path/some_file.txt"))
                expect(file_path.path).to_be_a(Path)
                expect(file_path.path).to_be(Path("/tmp/some_path/some_file.txt"))

        @describe("when created with a string")
        def _():
            @it("it sets the path")
            def _(tc: TestContext):
                file_path = FilePath("/tmp/some_path/some_file.txt")
                expect(file_path.path).to_be_a(Path)
                expect(file_path.path).to_be(Path("/tmp/some_path/some_file.txt"))

    @describe("when there is an existing file handler for the file")
    def _():
        @it("sets the handler")
        def _(tc: TestContext):
            file_path = FilePath("file_with_handler.txt")
            expect(file_path._handler).to_be(TxtHandler)

    @describe("when there is NO existing file handler for the file")
    def _():
        @it("sets the handler to None")
        def _(tc: TestContext):
            file_path = FilePath("file_with_handler.handler_with_no_extension")
            expect(file_path._handler).to_be(None)

    @describe("__str__")
    def _():
        @it("returns the path string")
        def _(self):
            file_path = FilePath(Path("/tmp/some_path/some_file.txt"))
            expect(str(file_path)).to_be("/tmp/some_path/some_file.txt")

    @describe("#exists")
    def _():
        @describe("the file doesn't exist")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                path = tc.test_directory / "some_file.txt"
                expect(path.exists()).to_be(False)

        @describe("the file exists")
        def _():
            @it("returns True")
            def _(tc: TestContext):
                path = tc.test_directory // "some_file.txt"
                with path.path.open("w") as fh:
                    fh.write("some string")
                expect(path.exists()).to_be(True)

    @describe("#touch")
    def _():
        @it("creates an empty file")
        def _(tc: TestContext):
            path = tc.test_directory // "some_file.txt"
            path.touch()
            expect(path.exists()).to_be(True)

    @describe("#get")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            file_path = tc.test_directory // "file_with_handler.txt"
            TxtHandler.save(file_path.path, "some text string\nsome other line\n")
            text = file_path.get()
            expect(text).to_be("some text string\nsome other line\n")

    @describe("#put")
    def _():
        @it("saves the string to file")
        def _(tc: TestContext):
            file_path = tc.test_directory // "file_with_handler.txt"
            file_path.put("some text string\nsome other line\n")
            text = TxtHandler.load(file_path.path)
            expect(file_path).to_be(an_existing_path())
            expect(text).to_be("some text string\nsome other line\n")
