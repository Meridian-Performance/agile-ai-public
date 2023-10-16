from pathlib import Path

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.data_marshalling.filesystem import remove_path
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, it, describe
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub

test_directory = Path("/tmp/agile_ai_tests")

class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


@pyne
def directory_path_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        remove_path(test_directory)
        expect(test_directory.exists()).to_be(False)

    @describe("#__init__")
    def _():
        @describe("when created with a Path")
        def _():
            @it("it sets the path")
            def _(tc: TestContext):
                directory_path = DirectoryPath("/tmp/some_path")
                expect(directory_path.path).to_be_a(Path)
                expect(directory_path.path).to_be(Path("/tmp/some_path"))

        @describe("when created with a string")
        def _():
            @it("it sets the path")
            def _(tc: TestContext):
                directory_path = DirectoryPath(Path("/tmp/some_path"))
                expect(directory_path.path).to_be(Path("/tmp/some_path"))

        @describe("__str__")
        def _():
            @it("returns the path string")
            def _(self):
                directory_path = DirectoryPath(Path("/tmp/some_path"))
                expect(str(directory_path)).to_be("/tmp/some_path")

        @describe("#exists")
        def _():
            @describe("the directory doesn't exist")
            def _():
                @it("returns False")
                def _(self):
                    path = DirectoryPath(test_directory / "some_non_existent_directory")
                    expect(path.exists()).to_be(False)

            @describe("the directory exists")
            def _():
                @it("returns True")
                def _(self):
                    (test_directory / "some_directory").mkdir(parents=True)
                    path = DirectoryPath(test_directory / "some_directory")
                    expect(path.exists()).to_be(True)

        @describe("#ensure_exists")
        def _():
            @it("creates the path and any parents")
            def _(tc: TestContext):
                path = DirectoryPath(test_directory / "some_directory" / "some_sub_directory")
                path.ensure_exists()
                expect(path.exists()).to_be(True)

        @describe("When a path is joined with a string using /")
        def _():
            @it("returns a DirectoryPath")
            def _(tc: TestContext):
                path = DirectoryPath(test_directory / "some_directory") / "some_sub_directory"
                expect(path).to_be_a(DirectoryPath)

            @it("concatenates the string to the path")
            def _(tc: TestContext):
                path = DirectoryPath(test_directory / "some_directory") / "some_sub_directory"
                expect(str(path)).to_be(f"{test_directory}/some_directory/some_sub_directory")

        @describe("When a path is joined with a string using //")
        def _():
            @it("concatenates the string to the path")
            def _(tc: TestContext):
                path = DirectoryPath(test_directory / "some_directory") / "some_sub_directory"
                expect(str(path)).to_be(f"{test_directory}/some_directory/some_sub_directory")

            @it("returns a FilePath")
            def _(tc: TestContext):
                path = DirectoryPath(test_directory / "some_directory") // "some_sub_directory"
                expect(path).to_be_a(FilePath)

    @describe("#__eq__")
    def _():
        @describe("when two directory paths are equal")
        def _():
            @it("returns True")
            def _(tc: TestContext):
                path_a = DirectoryPath(test_directory / "some_directory")
                path_b = DirectoryPath(test_directory / "some_directory")
                expect(path_a == path_b).to_be(True)
        @describe("when two directory paths are equal")
        def _():
            @it("returns true")
            def _(tc: TestContext):
                path_a = DirectoryPath(test_directory / "some_directory")
                path_b = DirectoryPath(test_directory / "some_other_directory")
                expect(path_a == path_b).to_be(False)
