import numpy as np
import pandas as pd

from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.memoization.warehouse_service import get_object, set_partition_name, register_object_class
from agile_ai.models.pandas_dataframe import PandasDataframe
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
    dataframe: pd.DataFrame

@pyne
def pandas_dataframe_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        register_object_class(PandasDataframe)
        tc.dataframe = pd.DataFrame(dict(some_values=np.arange(5)))

    @describe("When the object is stored")
    def _():
        @before_each
        def _(tc: TestContext):
            pdf = PandasDataframe().with_key_part(KeyLiteral("some_key_part"))
            pdf.path.put(tc.dataframe)
            pdf.put()

        @it("can be retrieved")
        def _(tc: TestContext):
            pdf = get_object(PandasDataframe, KeyLiteral("some_key_part"))
            expect(pdf.path.get()).to_be_a(pd.DataFrame)



