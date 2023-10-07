from dataclasses import dataclass
from typing import NamedTuple

from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.warehouse_key import KeyTuple, ObjectKey, KeyLiteral
from agile_ai.memoization.warehouse_object import ObjectOption, WarehouseObject
from agile_ai.processing.processor_io import IO
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class SomeInputA(WarehouseObject):
    pass


class SomeInputB(WarehouseObject):
    pass


class Inputs(IO):
    some_input_a: ObjectKey[SomeInputA]
    some_input_b: ObjectKey[SomeInputB]
    some_string_parameter: str
    some_float_parameter: float
    some_int_parameter: int


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    inputs: Inputs


@pyne
def processor_inputs_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @before_each
    def _(tc: TestContext):
        inputs = Inputs()
        inputs.some_input_a = ObjectOption.Key(SomeInputA, KeyLiteral("some_key_a"))
        inputs.some_input_b = ObjectOption.Key(SomeInputB, KeyLiteral("some_key_b"))
        inputs.some_string_parameter = "some_string"
        inputs.some_float_parameter = 4.0
        inputs.some_int_parameter = 1
        tc.inputs = inputs

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
