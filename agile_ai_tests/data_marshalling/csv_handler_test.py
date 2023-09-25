from pathlib import Path

import csv

from agile_ai.data_marshalling.csv_handler import CsvHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fdescribe, fit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    path: Path

@pyne
def csv_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.path = tc.test_directory.path / "file.csv"

    @describe("#load")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            with tc.path.open("w") as file:
                print('"a","b","c"', file=file)
                print('1,2,3', file=file)
            content = CsvHandler.load(tc.path)
            expect(content).to_have_length(2)
            expect(content[0]).to_be(["a", "b", "c"])
            expect(content[1]).to_be(["1", "2", "3"])

    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            CsvHandler.save(tc.path, [("a", "b", "c"), ("1", "2", "3")])
            expect(tc.path).to_be(an_existing_path())
            with tc.path.open("r") as file:
                lines = file.readlines()
            expect(lines).to_have_length(2)
            expect(lines[0]).to_be("a,b,c\n")
            expect(lines[1]).to_be("1,2,3\n")

    @describe("#matches")
    def _():
        @it("matches only .csv extensions")
        def _(tc: TestContext):
            expect(CsvHandler.matches("test.csv")).to_be(True)
            expect(CsvHandler.matches("test.csv_")).to_be(False)

    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.csv")._handler).to_be(CsvHandler)
