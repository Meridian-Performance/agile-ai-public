from pathlib import Path

import numpy as np
import pandas as pd

from agile_ai.data_marshalling.parquet_handler import ParquetHandler
from agile_ai.injection.decorators import Marker
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
    path: Path
    dataframe: pd.DataFrame


@pyne
def parequet_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.path = tc.test_directory.path / "dataframe.parquet"
        tc.dataframe = pd.DataFrame(dict(some_values=np.arange(5)))
    @describe("#load")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            tc.dataframe.to_parquet(str(tc.path))
            content: pd.DataFrame = ParquetHandler.load(tc.path)
            expect(content).to_be_a(pd.DataFrame)
            expect(len(content)).to_be(5)

    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            ParquetHandler.save(tc.path, tc.dataframe)
            content = pd.read_parquet(str(tc.path))
            expect(content).to_be_a(pd.DataFrame)
            expect(len(content)).to_be(5)

    @describe("#matches")
    def _():
        @it("matches only .parquet extensions")
        def _(tc: TestContext):
            expect(ParquetHandler.matches("test.parquet")).to_be(True)
            expect(ParquetHandler.matches("test.parquet_")).to_be(False)

    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.parquet")._handler).to_be(ParquetHandler)
