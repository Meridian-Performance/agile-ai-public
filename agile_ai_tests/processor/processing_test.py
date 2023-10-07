from agile_ai.injection.decorators import Marker
from agile_ai.memoization.warehouse_key import ObjectKey, KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_service import WarehouseService
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, describe, it
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub
from pynetest.expectations import expect


class TestContext(TCBase):
    __services__: Marker
    warehouse_service: WarehouseService

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


class SomeInputA(WarehouseObject):
    pass


class SomeInputB(WarehouseObject):
    pass


class SomeOutputA(WarehouseObject):
    pass


class SomeOutputB(WarehouseObject):
    pass


class ProcessorA(Processor):
    class Inputs(IO):
        some_input_a: ObjectOption[SomeInputA]
        some_input_b: ObjectOption[SomeInputB]

    class Outputs(IO):
        some_output_a: ObjectOption[SomeOutputA]
        some_output_b: ObjectOption[SomeOutputB]

    def perform(self, inputs: Inputs, outputs: Outputs):
        outputs.some_output_a.set(SomeOutputA())
        outputs.some_output_b.set(SomeOutputB())


@pyne
def processing_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.warehouse_service.set_warehouse_directory(tc.test_directory / "warehouse")
        tc.warehouse_service.set_partition_name("some_partition_name")

    @describe("#perform (super)")
    def _():
        @it("calls perform")
        def _(tc: TestContext):
            some_input_a = SomeInputA().with_key_part(KeyLiteral("some_input_a"))
            some_input_b = SomeInputA().with_key_part(KeyLiteral("some_input_b"))
            tc.warehouse_service.put_object(some_input_a)
            tc.warehouse_service.put_object(some_input_b)
            inputs = ProcessorA.Inputs()
            inputs.some_input_a = ObjectOption(some_input_a)
            inputs.some_input_b = ObjectOption(some_input_b)
            outputs: ProcessorA.Outputs = ProcessorA().perform_super(inputs)
            expect(outputs).to_be_a(ProcessorA.Outputs)
            key_part = inputs.get_key()
            expect(outputs.some_output_a.object_key).to_be(ObjectKey(SomeOutputA, key_part))
            expect(outputs.some_output_b.object_key).to_be(ObjectKey(SomeOutputB, key_part))
            expect(tc.warehouse_service.has_object(outputs.some_output_a.object_key)).to_be(True)
            expect(tc.warehouse_service.has_object(outputs.some_output_b.object_key)).to_be(True)

    @describe("#resolve")
    def _():
        @it("")
        def _(tc: TestContext):
            ...
