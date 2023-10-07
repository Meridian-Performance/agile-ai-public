from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.warehouse_key import ObjectKey, KeyTuple, KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fdescribe, fit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


class SomeWarehouseObject(WarehouseObject):
    pass


@pyne
def warehouse_key_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("KeyLiteral")
    def _():
        @describe("#to_storage")
        def _():
            @it("serializes a string KeyLiteral to a string")
            def _(tc: TestContext):
                key_literal = KeyLiteral("some_string")
                expect(key_literal.to_storage()).to_be('"some_string"')

            @it("serializes a int KeyLiteral to a string")
            def _(tc: TestContext):
                key_literal = KeyLiteral(5)
                expect(key_literal.to_storage()).to_be('"int:5"')

            @it("serializes a float KeyLiteral to a string")
            def _(tc: TestContext):
                key_literal = KeyLiteral(5.0)
                expect(key_literal.to_storage()).to_be('"float:5.0"')

        @describe(":from_storage")
        def _():
            @it("deserializes a string KeyLiteral from a string")
            def _(tc: TestContext):
                expect(KeyLiteral.from_storage('"some_string"')).to_be_a(KeyLiteral)
                expect(KeyLiteral.from_storage('"some_string"').literal).to_be_a(str)
                expect(KeyLiteral.from_storage('"some_string"').literal).to_be("some_string")

            @it("deserializes a float KeyLiteral from a string")
            def _(tc: TestContext):
                expect(KeyLiteral.from_storage('"float:5.0"')).to_be_a(KeyLiteral)
                expect(KeyLiteral.from_storage('"float:5.0"').literal).to_be_a(float)
                expect(KeyLiteral.from_storage('"float:5.0"').literal).to_be(5.0)

            @it("deserializes a float KeyLiteral from a string")
            def _(tc: TestContext):
                expect(KeyLiteral.from_storage('"int:5"')).to_be_a(KeyLiteral)
                expect(KeyLiteral.from_storage('"int:5"').literal).to_be_a(int)
                expect(KeyLiteral.from_storage('"int:5"').literal).to_be(5)

    @describe("KeyTuple")
    def _():
        @describe("#to_storage")
        def _():
            @describe("when it only contain literals")
            def _():
                @it("serializes the literals as a tuple string")
                def _(tc: TestContext):
                    key_tuple = KeyTuple([KeyLiteral("some_string"), KeyLiteral(5.0), KeyLiteral(1)])
                    expect(key_tuple.to_storage()).to_be('("some_string", "float:5.0", "int:1")')

            @describe("when it contains a KeyTuple")
            def _():
                @it("serializes the literals as a tuple string")
                def _(tc: TestContext):
                    key_tuple = KeyTuple([KeyLiteral("some_string"), KeyTuple([KeyLiteral(5.0), KeyLiteral(1)])])
                    expect(key_tuple.to_storage()).to_be('("some_string", ("float:5.0", "int:1"))')

            @describe("when it contains an ObjectKey")
            def _():
                @it("serializes the literals as a tuple string")
                def _(tc: TestContext):
                    key_tuple = KeyTuple([ObjectKey(SomeWarehouseObject, KeyLiteral("some_string")), KeyTuple([KeyLiteral(5.0), KeyLiteral(1)])])
                    expect(key_tuple.to_storage()).to_be('(["SomeWarehouseObject", "some_string"], ("float:5.0", "int:1"))')

        @describe(":from_storage")
        def _():
            @describe("when it only contain literals")
            def _():
                @it("deserializes the literals")
                def _(tc: TestContext):
                    key_tuple = KeyTuple.from_storage('("some_string", "float:5.0", "int:1")')
                    expect(key_tuple.key_parts).to_have_length(3)
                    expect(key_tuple.key_parts[0]).to_be(KeyLiteral("some_string"))
                    expect(key_tuple.key_parts[1]).to_be(KeyLiteral(5.0))
                    expect(key_tuple.key_parts[2]).to_be(KeyLiteral(1))

            @describe("when it contains a KeyTuple")
            def _():
                @it("serializes the literals as a tuple string")
                def _(tc: TestContext):
                    key_tuple = KeyTuple.from_storage('("some_string", ("float:5.0", "int:1"))')
                    expect(key_tuple.key_parts).to_have_length(2)
                    expect(key_tuple.key_parts[0]).to_be(KeyLiteral("some_string"))
                    expect(key_tuple.key_parts[1]).to_be_a(KeyTuple)
                    expect(key_tuple.key_parts[1].key_parts).to_have_length(2)

    @describe("ObjectKey")
    def _():
        @describe("#to_storage")
        def _():
            @describe("when the key part is a literal")
            def _():
                @it("serializes it as an ObjectKey string")
                def _(tc: TestContext):
                    object_key = ObjectKey(SomeWarehouseObject, KeyLiteral("some_string"))
                    expect(object_key.to_storage()).to_be('["SomeWarehouseObject", "some_string"]')

        @describe(":from_storage")
        def _():
            @describe("when the key part is a literal")
            def _():
                @it("deserializes it as an ObjectKey")
                def _(tc: TestContext):
                    object_key = ObjectKey.from_storage('["SomeWarehouseObject", "some_string"]')
                    expect(object_key.object_cls_name).to_be("SomeWarehouseObject")
                    expect(object_key.key_part).to_be_a(KeyLiteral)
                    key_literal: KeyLiteral = object_key.key_part
                    expect(key_literal.literal).to_be("some_string")

            @describe("when the key part is a tuple")
            def _():
                @it("deserializes it as an ObjectKey")
                def _(tc: TestContext):
                    object_key = ObjectKey.from_storage('["SomeWarehouseObject", ("some_string_a", "some_string_b")]')
                    expect(object_key.object_cls_name).to_be("SomeWarehouseObject")
                    expect(object_key.key_part).to_be_a(KeyTuple)
                    key_tuple: KeyTuple = object_key.key_part
                    expect(key_tuple.key_parts).to_have_length(2)

            @describe("when the key part is an ObjectKey")
            def _():
                @it("deserializes it as an ObjectKey")
                def _(tc: TestContext):
                    object_key = ObjectKey.from_storage('["SomeWarehouseObject", ["SomeWarehouseObject", "some_string"]]')
                    expect(object_key.object_cls_name).to_be("SomeWarehouseObject")
                    expect(object_key.key_part).to_be_a(ObjectKey)
                    expect(object_key.key_part.object_cls_name).to_be("SomeWarehouseObject")
