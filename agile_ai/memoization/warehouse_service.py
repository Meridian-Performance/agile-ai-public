from typing import Type, List, TypeVar, Optional

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.decorators import get_service
from agile_ai.injection.interfaces import Service
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import ObjectKey, StorageKey, KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject

WarehouseObjectT = TypeVar("WarehouseObjectT", bound=WarehouseObject)


class WarehouseService(Service):
    partition_order: List[str]
    warehouse_directory: DirectoryPath

    def __init__(self):
        self.object_class_by_name = dict()

    def register_object_class(self, object_cls: Type[WarehouseObject]):
        self.object_class_by_name[object_cls.get_class_name()] = object_cls

    def set_warehouse_directory(self, warehouse_directory: DirectoryPath):
        self.warehouse_directory = warehouse_directory

    def set_partition_name(self, partition_name: str):
        self.partition_order = [partition_name]

    def set_partition_order(self, partition_order: List[str]):
        self.partition_order = partition_order

    @property
    def partition_name(self) -> str:
        return self.partition_order[0]

    @property
    def partition_directory(self) -> DirectoryPath:
        return self.warehouse_directory / self.partition_name

    def put_object(self, object_instance: WarehouseObject, partition_name: Optional[str] = None):
        object_instance.save(object_instance.get_object_key(partition_name))

    def get_object(self, key: ObjectKey):
        class_name = key.object_cls_name
        object_class = self.lookup_class_by_name(class_name)
        key_with_partition = self.find_object_key_with_partition(key)
        if key_with_partition is None:
            raise KeyError(
                f"Object of class '{class_name}' with key {key} was not found in partitions {self.partition_order}")
        return object_class.load(key_with_partition)

    def lookup_class_by_name(self, class_name: str) -> Type[WarehouseObject]:
        object_class = self.object_class_by_name.get(class_name)
        if object_class is None:
            raise ModuleNotFoundError(f"Unable to lookup class for `{class_name}`, did you register it?")
        return object_class

    def find_object_key_with_partition(self, key: ObjectKey) -> Optional[ObjectKey]:
        partition_names = [key.partition_name] if key.partition_name is not None else self.partition_order
        for partition_name in partition_names:
            key_with_partition = key.copy(partition_name=partition_name)
            object_path = self.get_object_path(key_with_partition)
            if (object_path // "metadata.json").exists():
                return key_with_partition
        return None

    def has_object(self, key: ObjectKey):
        key_with_partition = self.find_object_key_with_partition(key)
        return key_with_partition is not None

    def get_object_class_path(self, object_key: ObjectKey) -> DirectoryPath:
        object_cls_name = object_key.object_cls_name
        partition_name = object_key.partition_name if object_key.partition_name else self.partition_name
        return self.warehouse_directory / partition_name / object_cls_name

    def get_object_path(self, key: ObjectKey) -> DirectoryPath:
        return self.get_object_class_path(key) / key.get_key_part().get_storage_string()

    def get_object_options(self, object_class: Type[WarehouseObjectT]) -> List[ObjectOption[WarehouseObjectT]]:
        key_set = set()
        object_options = []
        for partition_name in self.partition_order:
            class_directory = self.get_object_class_path(
                ObjectKey(object_class, partition_name=partition_name, key_part=None))
            if not class_directory.exists():
                continue
            for path in class_directory.path.iterdir():
                md5_hex = path.name
                key_part = StorageKey(md5_hex)
                object_key = ObjectKey(object_class, key_part, partition_name=partition_name)
                key = object_key.to_storage()
                if key in key_set:
                    continue
                key_set.add(key)
                object_option = ObjectOption(object_key)
                object_options.append(object_option)
        return object_options


def set_partition_name(partition_name: str):
    from agile_ai.injection.decorators import get_service
    warehouse_service = get_service(WarehouseService)
    warehouse_service.set_partition_name(partition_name)


def set_warehouse_directory(warehouse_directory: DirectoryPath):
    from agile_ai.injection.decorators import get_service
    warehouse_service = get_service(WarehouseService)
    warehouse_service.set_warehouse_directory(warehouse_directory)


def register_object_class(object_class):
    from agile_ai.injection.decorators import get_service
    warehouse_service = get_service(WarehouseService)
    warehouse_service.register_object_class(object_class)


def get_object(object_class: Type[WarehouseObject], key_part: KeyPart) -> WarehouseObjectT:
    warehouse_service = get_service(WarehouseService)
    return warehouse_service.get_object(ObjectKey(object_class, key_part))
