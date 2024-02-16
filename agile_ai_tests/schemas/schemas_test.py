import numpy as np
import pandas as pd

from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.schemas.dataframe_schema import DataframeSchema, StringColumn, FloatColumn, IntColumn, BoolColumn
from agile_ai_tests.test_helpers.pyne_future import exactly_equal_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class SomeSchema(DataframeSchema):
    label: StringColumn
    some_int: IntColumn
    some_float: FloatColumn
    some_bool: BoolColumn


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    some_schema: SomeSchema


@pyne
def schemas_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @before_each
    def _(tc: TestContext):
        tc.some_schema = SomeSchema(pd.DataFrame(data=dict(
            label=[f"{i}_label" for i in range(5)],
            some_int=np.arange(5, dtype=int),
            some_float=np.arange(5, dtype=float),
            some_bool=np.arange(5, dtype=int) % 2 == 0
        )))

    @describe("when an column is accessed")
    def _():
        @it("returns the series")
        def _(tc: TestContext):
            expect(list(tc.some_schema.label.values)).to_match_list(tc.some_schema.df.label.values)
            expect(list(tc.some_schema.some_int.values)).to_be(
                exactly_equal_to_array(tc.some_schema.df.some_int.values))
            expect(list(tc.some_schema.some_float.values)).to_be(
                exactly_equal_to_array(tc.some_schema.df.some_float.values))
            expect(list(tc.some_schema.some_bool.values)).to_be(
                exactly_equal_to_array(tc.some_schema.df.some_bool.values))

    @describe("when the index is accessed")
    def _():
        @it("returns the index")
        def _(tc: TestContext):
            expect(list(tc.some_schema.index.values)).to_be(exactly_equal_to_array(tc.some_schema.df.index.values))

    @describe("when a dataframe function is used")
    def _():
        @it("operates as if it was performed on the inner df")
        def _(tc: TestContext):
            expect(tc.some_schema.iloc[2]).to_match_list(tc.some_schema.df.iloc[2])

    @describe("when a function that returns a df is used")
    def _():
        @it("returns a Schema wrapped dataframe")
        def _(tc: TestContext):
            sorted_schema = tc.some_schema.sort_values(by="some_int")
            expect(sorted_schema).to_be_a(SomeSchema)
            expect(sorted_schema.some_int.array).to_be(exactly_equal_to_array(tc.some_schema.df.sort_values(by="some_int").some_int.array))

    @describe(":from_columns")
    def _():
        @it("creates the df with columns in order as defined by the annotation")
        def _(tc: TestContext):
            some_schema = SomeSchema.from_columns([f"{i}_label" for i in range(5)], np.arange(5, dtype=int), np.arange(5, dtype=float), np.arange(5, dtype=int) % 2 == 0)
            expect(some_schema.label[0]).to_be_a(str)
            expect(some_schema.some_float[0]).to_be_a(float)
            expect(some_schema.some_int[0]).to_be_a(np.int64)
            expect(some_schema.some_bool[0]).to_be_a(np.bool_)

    @describe(":zeros")
    def _():
        @it("creates the df with columns in order as defined by the annotation")
        def _(tc: TestContext):
            some_schema = SomeSchema.zeros(5)
            expect(some_schema).to_have_length(5)
            expect(some_schema.label[0]).to_be_a(str)
            expect(some_schema.some_float[0]).to_be_a(float)
            expect(some_schema.some_int[0]).to_be_a(np.int64)
            expect(some_schema.some_bool[0]).to_be_a(np.bool_)
