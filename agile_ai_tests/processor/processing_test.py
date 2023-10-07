from agile_ai.injection.decorators import Marker
from agile_ai.memoization.warehouse_key import ObjectKey
from agile_ai.memoization.warehouse_object import ObjectOption, WarehouseObject
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, describe, it
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


class SomeInputA(WarehouseObject):
    pass


class SomeOutputA(WarehouseObject):
    pass


class SomeOutputB(WarehouseObject):
    pass


class ProcessorA(Processor):
    class Inputs(IO):
        some_input_a: ObjectOption[SomeInputA]
        some_input_b: ObjectOption[SomeInputA]

    class Outputs(IO):
        some_output_a: ObjectOption[SomeOutputA]
        some_output_b: ObjectOption[SomeOutputA]

    def perform(self, inputs: Inputs) -> Outputs:
        pass


#@pyne
def processing_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#resolve")
    def _():
        @it("")
        def _(tc: TestContext):
            ...

