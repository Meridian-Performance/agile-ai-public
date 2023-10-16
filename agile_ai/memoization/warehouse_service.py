from typing import Type, List, TypeVar

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.interfaces import Service
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import ObjectKey, KeyLiteral, StorageKey
from agile_ai.memoization.warehouse_object import WarehouseObject
WarehouseObjectT = TypeVar("WarehouseObjectT", bound=WarehouseObject)


class WarehouseService(Service):
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
        class_name = key.object_cls_name
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

    def get_object_class_path(self, object_cls_name: str) -> DirectoryPath:
        return self.warehouse_directory / self.partition_name / object_cls_name

    def get_object_path(self, key: ObjectKey) -> DirectoryPath:
        return self.get_object_class_path(key.object_cls_name) / key.get_key_part().get_storage_string()
    def get_object_options(self, object_class: Type[WarehouseObjectT]) -> List[ObjectOption[WarehouseObjectT]]:
        class_directory = self.get_object_class_path(object_class.get_class_name())
        object_options = []
        for path in class_directory.path.iterdir():
            md5_hex = path.name
            key_part = StorageKey(md5_hex)
            object_key = ObjectKey(object_class, key_part)
            object_option = ObjectOption(object_key)
            object_options.append(object_option)
        return object_options



def register_object_class(object_class):
    from agile_ai.injection.decorators import get_service
    warehouse_service = get_service(WarehouseService)
    warehouse_service.register_object_class(object_class)
