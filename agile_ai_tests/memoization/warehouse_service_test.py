from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.decorators import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import ObjectKey, KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import WarehouseService
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class SomeOtherWarehouseObject(WarehouseObject):
    __metadata__: Marker
    some_other_data: str


class SomeWarehouseObject(WarehouseObject):
    __metadata__: Marker
    some_data: str

    __objects__: Marker
    some_other_object: ObjectOption[SomeOtherWarehouseObject]

    def fetch(self, directory_path: DirectoryPath):
        self.some_file_data = (directory_path // "some_file.json").get()

    def store(self, directory_path: DirectoryPath):
        (directory_path // "some_file.json").put(self.some_file_data)


class TestContext(TCBase):
    __services__: Marker
    warehouse_service: WarehouseService

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    object_key: ObjectKey
    object_path: DirectoryPath
    warehouse_object: SomeWarehouseObject


@pyne
def warehouse_service_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("#set_warehouse_directory")
    def _():
        @it("sets the warehouse directory")
        def _(tc: TestContext):
            tc.warehouse_service.set_warehouse_directory(tc.test_directory / "some_warehouse_directory")
            expect(tc.warehouse_service.warehouse_directory).to_be(tc.test_directory / "some_warehouse_directory")

    @describe("#set_partition_name")
    def _():
        @it("...")
        def _(tc: TestContext):
            tc.warehouse_service.set_partition_name("some_partition_name")
            expect(tc.warehouse_service.partition_name).to_be("some_partition_name")

    @describe("when the warehouse is configured")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.warehouse_service.set_warehouse_directory(tc.test_directory / "some_warehouse_directory")
            tc.warehouse_service.set_partition_name("some_partition_name")
            tc.warehouse_service.register_object_class(SomeWarehouseObject)

        @describe("#get_object_path")
        def _():
            @it("return the directory with format warehouse_directory/partition_name/ObjectClassName/some_object_key_part_hex")
            def _(tc: TestContext):
                key_part = KeyLiteral("some_object_key_part")
                object_key = ObjectKey(SomeWarehouseObject, key_part)
                md5_hex = key_part.get_storage_string()
                object_directory = tc.warehouse_service.get_object_path(object_key)
                expect(object_directory).to_be(
                    tc.test_directory / "some_warehouse_directory" / "some_partition_name" / "SomeWarehouseObject" / md5_hex
                )

        @describe("#put_object")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.warehouse_object = SomeWarehouseObject()
                tc.warehouse_object.some_data = "some_data_value"
                tc.warehouse_object.some_file_data = "some_file_data_value"
                tc.warehouse_object.set_key_part(KeyLiteral("some_key_part"))
                tc.warehouse_object.some_other_object = ObjectOption(ObjectKey(SomeOtherWarehouseObject, KeyLiteral("some_other_object_key")))

            @it("stores the metadata with the object_key")
            def _(tc: TestContext):
                tc.warehouse_service.put_object(tc.warehouse_object)
                object_directory = tc.warehouse_service.get_object_path(tc.warehouse_object.get_object_key())
                metadata_path = object_directory // "metadata.json"
                expect(metadata_path).to_be(an_existing_path())
                metadata_dict = metadata_path.get()
                expect(metadata_dict["some_data"]).to_be("some_data_value")
                expect(metadata_dict["key_part"]).to_be('"some_key_part"')
                expect(metadata_dict["class_name"]).to_be("SomeWarehouseObject")

            @it("stores the metadata with the reference object_key")
            def _(tc: TestContext):
                tc.warehouse_service.put_object(tc.warehouse_object)
                object_directory = tc.warehouse_service.get_object_path(tc.warehouse_object.get_object_key())
                metadata_path = object_directory // "metadata.json"
                metadata_dict = metadata_path.get()
                other_object_key = ObjectKey(SomeOtherWarehouseObject, KeyLiteral("some_other_object_key"))
                expect(metadata_dict["some_other_object"]).to_be(other_object_key.to_storage())


            @it("persists data using stores")
            def _(tc: TestContext):
                tc.warehouse_service.put_object(tc.warehouse_object)
                object_directory = tc.warehouse_service.get_object_path(tc.warehouse_object.get_object_key())
                expect(object_directory // "some_file.json").to_be(an_existing_path())
                expect((object_directory // "some_file.json").get()).to_be("some_file_data_value")

        @describe("#has_object")
        def _():
            @before_each
            def _(tc: TestContext):
                key_part = KeyLiteral("some_object_key_part")
                tc.object_key = ObjectKey(SomeWarehouseObject, key_part)
                tc.object_path = tc.warehouse_service.get_object_path(tc.object_key)

            @describe("when metadata.json exists at the object path")
            def _():
                @it("returns True")
                def _(tc: TestContext):
                    (tc.object_path // "metadata.json").touch()
                    expect(tc.warehouse_service.has_object(tc.object_key)).to_be(True)

            @describe("when metadata.json does not exist at the object path")
            def _():
                @it("returns False")
                def _(tc: TestContext):
                    expect(tc.warehouse_service.has_object(tc.object_key)).to_be(False)

        @describe("#get_object")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.warehouse_object = SomeWarehouseObject()
                tc.warehouse_service.register_object_class(SomeOtherWarehouseObject)
                tc.warehouse_object.some_data = "some_data_value"
                tc.warehouse_object.some_file_data = "some_file_data_value"
                tc.warehouse_object.set_key_part(KeyLiteral("some_key_part"))
                some_other_object = SomeOtherWarehouseObject().with_key_part(KeyLiteral("some_other_object_key"))
                tc.warehouse_object.some_other_object = ObjectOption(some_other_object)
                tc.warehouse_service.put_object(tc.warehouse_object)
                tc.warehouse_service.put_object(some_other_object)

            @it("returns an instance of the cls from the ObjectKey")
            def _(tc: TestContext):
                warehouse_object = tc.warehouse_service.get_object(tc.warehouse_object.get_object_key())
                expect(warehouse_object).to_be_a(SomeWarehouseObject)

            @it("sets the values from the metadata")
            def _(tc: TestContext):
                warehouse_object: SomeWarehouseObject = tc.warehouse_service.get_object(
                    tc.warehouse_object.get_object_key())
                expect(warehouse_object.some_data).to_be("some_data_value")
                expect(warehouse_object.key_part).to_be_a(KeyLiteral)
                expect(warehouse_object.key_part.to_storage()).to_be('"some_key_part"')

            @it("sets the ObjectOption keys from the metadata")
            def _(tc: TestContext):
                warehouse_object: SomeWarehouseObject = tc.warehouse_service.get_object(
                    tc.warehouse_object.get_object_key())
                expect(warehouse_object.some_other_object).to_be_a(ObjectOption)
                expect(warehouse_object.some_other_object.object_key).to_be_a(ObjectKey)
                expect(warehouse_object.some_other_object.object_key).to_be(tc.warehouse_object.some_other_object.object_key)
                expect(warehouse_object.some_other_object.is_present()).to_be(True)

            @it("persists data using fetch")
            def _(tc: TestContext):
                warehouse_object: SomeWarehouseObject = tc.warehouse_service.get_object(
                    tc.warehouse_object.get_object_key())
                expect(warehouse_object.some_file_data).to_be("some_file_data_value")

        @describe("#get_object_options")
        def _():
            @before_each
            def _(tc: TestContext):
                warehouse_object = SomeWarehouseObject()
                some_other_object = SomeOtherWarehouseObject().with_key_part(KeyLiteral("some_other_object_key"))
                warehouse_object.some_data = "some_data_value"
                warehouse_object.some_file_data = "some_file_data_value"
                warehouse_object.set_key_part(KeyLiteral("some_key_part"))
                warehouse_object.some_other_object = ObjectOption(some_other_object)
                tc.warehouse_service.put_object(warehouse_object)
                warehouse_object = SomeWarehouseObject()
                warehouse_object.some_data = "some_other_data_value"
                warehouse_object.some_file_data = "some_other_file_data_value"
                warehouse_object.set_key_part(KeyLiteral("some_other_key_part"))
                warehouse_object.some_other_object = ObjectOption(some_other_object)
                tc.warehouse_service.put_object(warehouse_object)
                tc.warehouse_service.put_object(some_other_object)

            @it("returns a list of ObjectOptions for every warehouse object of the specified type")
            def _(tc: TestContext):
                object_options = tc.warehouse_service.get_object_options(SomeWarehouseObject)
                expect(object_options).to_have_length(2)
                expect(object_options[0]).to_be_a(ObjectOption)
                expect(object_options[0].get()).to_be_a(SomeWarehouseObject)

