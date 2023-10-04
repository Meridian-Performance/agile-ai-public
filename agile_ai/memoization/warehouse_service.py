from typing import Type

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.memoization.warehouse_key import ObjectKey
from agile_ai.memoization.warehouse_object import WarehouseObject


class WarehouseService:
    partition_name: str
    warehouse_directory: DirectoryPath

    def __init__(self):
        self.object_class_by_name = dict()

    def register_object_class(self, object_cls: Type[WarehouseObject]):
        self.object_class_by_name[object_cls.get_class_name()] = object_cls

    def set_warehouse_directory(self, warehouse_directory: DirectoryPath):
        self.warehouse_directory = warehouse_directory

    def set_partition_name(self, partition_name: str):
        self.partition_name = partition_name

    @property
    def partition_directory(self) -> DirectoryPath:
        return self.warehouse_directory / self.partition_name

    def put_object(self, object_instance: WarehouseObject):
        object_path = self.get_object_path(object_instance.get_object_key())
        object_instance.save(object_path)

    def get_object(self, key: ObjectKey):
        class_name = key.get_class_name()
        object_class = self.lookup_class_by_name(class_name)
        object_path = self.get_object_path(key)
        return object_class.load(object_path)

    def lookup_class_by_name(self, class_name: str) -> Type[WarehouseObject]:
        object_class = self.object_class_by_name.get(class_name)
        if object_class is None:
            raise ModuleNotFoundError(f"Unable to lookup class for `{class_name}`, did you register it?")
        return object_class

    def has_object(self, key: ObjectKey):
        object_path = self.get_object_path(key)
        return (object_path // "metadata.json").exists()

    def get_object_path(self, key: ObjectKey) -> DirectoryPath:
        return self.warehouse_directory / self.partition_name / key.get_class_name() / key.get_key_part().get_storage_string()
