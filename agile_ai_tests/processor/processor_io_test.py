from dataclasses import dataclass
from typing import NamedTuple

from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.warehouse_key import KeyTuple, ObjectKey, KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_service import WarehouseService
from agile_ai.processing.processor_io import IO
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class SomeInputA(WarehouseObject):
    def fetch(self, directory_path):
        pass

    def store(self, directory_path):
        pass


class SomeInputB(WarehouseObject):
    def fetch(self, directory_path):
        pass

    def store(self, directory_path):
        pass


class Inputs(IO):
    some_input_a: ObjectOption[SomeInputA]
    some_input_b: ObjectOption[SomeInputB]
    some_string_parameter: str
    some_float_parameter: float
    some_int_parameter: int


class TestContext(TCBase):
    __services__: Marker
    warehouse_service: WarehouseService

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    inputs: Inputs
    outputs: Inputs


@pyne
def processor_io_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @before_each
    def _(tc: TestContext):
        tc.warehouse_service.set_warehouse_directory(tc.test_directory / "warehouse_directory")
        tc.warehouse_service.set_partition_name("some_partition_name")
        inputs = Inputs()
        inputs.some_input_a = ObjectOption.Key(SomeInputA, KeyLiteral("some_key_a"))
        inputs.some_input_b = ObjectOption.Key(SomeInputB, KeyLiteral("some_key_b"))
        inputs.some_string_parameter = "some_string"
        inputs.some_float_parameter = 4.0
        inputs.some_int_parameter = 1
        tc.inputs = inputs
        tc.outputs = inputs

    @describe("#get_key")
    def _():
        @it("concatenates all of the inputs elements, in order")
        def _(tc: TestContext):
            key_tuple = tc.inputs.get_key()
            expect(key_tuple).to_be_a(KeyTuple)
            expect(key_tuple.key_parts).to_have_length(5)
            expect(key_tuple.key_parts[0]).to_be_a(ObjectKey)
            expect(key_tuple.key_parts[1]).to_be_a(ObjectKey)
            expect(key_tuple.key_parts[2]).to_be_a(KeyLiteral)
            expect(key_tuple.key_parts[3]).to_be_a(KeyLiteral)
            expect(key_tuple.key_parts[4]).to_be_a(KeyLiteral)
            expect(key_tuple.to_storage()).to_be(
                '(["SomeInputA", "some_key_a"], ["SomeInputB", "some_key_b"], "some_string", "float:4.0", "int:1")')

    @describe("#all_options_present")
    def _():
        @before_each
        def _(tc: TestContext):
            some_input_a = SomeInputA().with_key_part(KeyLiteral("some_key_a"))
            tc.warehouse_service.put_object(some_input_a)

        @describe("when all options are present")
        def _():
            @before_each
            def _(tc: TestContext):
                some_input_b = SomeInputB().with_key_part(KeyLiteral("some_key_b"))
                tc.warehouse_service.put_object(some_input_b)

            @it("returns True")
            def _(tc: TestContext):
                expect(tc.inputs.all_options_present()).to_be(True)

        @describe("when some options are empty")
        def _():
            @it("returns False")
            def _(tc: TestContext):
                expect(tc.inputs.all_options_present()).to_be(False)

    @describe("#store_options")
    def _():
        @it("puts all object instances stored in object options")
        def _(tc: TestContext):
            some_input_a = SomeInputA().with_key_part(KeyLiteral("some_key_a"))
            some_input_b = SomeInputB().with_key_part(KeyLiteral("some_key_a"))
            tc.outputs.some_input_a.set(some_input_a)
            tc.outputs.some_input_b.set(some_input_b)
            expect(tc.warehouse_service.has_object(some_input_a.get_object_key()))
            expect(tc.warehouse_service.has_object(some_input_b.get_object_key()))
