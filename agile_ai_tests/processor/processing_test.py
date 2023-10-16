from typing import Callable

from agile_ai.injection.decorators import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import ObjectKey, KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import WarehouseService
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, describe, it, with_stubs
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import AttachedSpy, attach_spy
from pynetest.test_doubles.stub import MegaStub


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
        pass

    inputs: Inputs
    resolve: Callable[..., Outputs]


class TestContext(TCBase):
    __services__: Marker
    warehouse_service: WarehouseService

    __stubs__: Marker
    stubs: MegaStub
    perform_stub: AttachedSpy

    __other__: Marker
    inputs: ProcessorA.Inputs
    processor: ProcessorA

@pyne
def processing_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.warehouse_service.set_warehouse_directory(tc.test_directory / "warehouse")
        tc.warehouse_service.set_partition_name("some_partition_name")
        some_input_a = SomeInputA().with_key_part(KeyLiteral("some_input_a"))
        some_input_b = SomeInputA().with_key_part(KeyLiteral("some_input_b"))
        tc.warehouse_service.put_object(some_input_a)
        tc.warehouse_service.put_object(some_input_b)
        tc.processor = ProcessorA()
        inputs = tc.processor.inputs
        inputs.some_input_a = ObjectOption(some_input_a)
        inputs.some_input_b = ObjectOption(some_input_b)
        tc.inputs = inputs

    @describe("#perform (super)")
    def _():
        @it("calls perform")
        def _(tc: TestContext):
            outputs: ProcessorA.Outputs = ProcessorA().perform_super(tc.inputs)
            expect(outputs).to_be_a(ProcessorA.Outputs)
            key_part = tc.inputs.get_key()
            expect(outputs.some_output_a.object_key).to_be(ObjectKey(SomeOutputA, key_part))
            expect(outputs.some_output_b.object_key).to_be(ObjectKey(SomeOutputB, key_part))
            expect(tc.warehouse_service.has_object(outputs.some_output_a.object_key)).to_be(True)
            expect(tc.warehouse_service.has_object(outputs.some_output_b.object_key)).to_be(True)

    @describe("#resolve")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.stubs = attach_spy(tc.processor, "perform")

        @describe("when all outputs exist")
        def _():
            @before_each
            def _(tc: TestContext):
                key_part = tc.inputs.get_key()
                tc.warehouse_service.put_object(SomeOutputA().with_key_part(key_part))
                tc.warehouse_service.put_object(SomeOutputB().with_key_part(key_part))

            @it("doesn't call perform")
            @with_stubs
            def _(tc: TestContext):
                outputs = tc.processor.resolve()
                expect(outputs).to_be_a(ProcessorA.Outputs)
                expect(tc.processor.perform).was_not_called()

        @describe("when any outputs is missing")
        def _():
            @it("calls perform")
            @with_stubs
            def _(tc: TestContext):
                outputs = tc.processor.resolve()
                expect(outputs).to_be_a(ProcessorA.Outputs)
                expect(tc.processor.perform).was_called()