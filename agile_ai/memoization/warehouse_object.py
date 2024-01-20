from typing import TypeVar, Optional

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.decorators import get_service
from agile_ai.memoization.warehouse_key import ObjectKey, KeyPart
from agile_ai.processing.processor_io import ObjectWithOptions
from agile_ai.utilities.introspection import Introspection

WarehouseObjectT = TypeVar("WarehouseObjectT", bound="WarehouseObject")


class WarehouseObject(ObjectWithOptions):

    def set_key_part(self, key_part: KeyPart):
        self.object_key.key_part = key_part
        return self

    def with_key_part(self, key_part: KeyPart):
        self.set_key_part(key_part)
        return self

    def with_partition_name(self, partition_name: str):
        self.object_key.with_partition_name(partition_name)
        return self

    @property
    def key_part(self) -> KeyPart:
        return self.object_key.key_part

    def __init__(self, key_part: Optional[KeyPart] = None, partition_name: Optional[str] = None):
        self.object_key = ObjectKey(self.get_class(), key_part, partition_name=partition_name)

    def _copy_metadata(self, source_dict: dict, destination_dict: dict):
        cls = self.get_class()
        marker_groups = Introspection.get_marker_groups(cls)
        metadata_keys = set(marker_groups.get("__metadata__", {}).keys())
        metadata_keys.add("key_part")
        metadata_keys.add("class_name")
        for metadata_key in metadata_keys:
            metadata_value = source_dict.get(metadata_key)
            destination_dict[metadata_key] = metadata_value
        return destination_dict

    def get_metadata_dict(self) -> dict:
        source_dict = dict(self.__dict__)
        source_dict["key_part"] = self.key_part
        return self._copy_metadata(source_dict, destination_dict=dict())

    def set_metadata_dict(self, metadata_dict):
        self._copy_metadata(metadata_dict, self.__dict__)

    @classmethod
    def get_class(cls):
        return cls

    @classmethod
    def get_class_name(cls):
        return Introspection.get_class_name(cls)

    def get_object_key(self, partition_name: Optional[str] = None) -> ObjectKey:
        return self.object_key.with_partition_name(partition_name)

    @classmethod
    def load(cls: WarehouseObjectT, object_key: ObjectKey):
        class_instance: WarehouseObjectT = cls(object_key.key_part, object_key.partition_name)
        directory_path = class_instance.get_object_path()
        metadata_dict = (directory_path // "metadata.json").get()
        metadata_dict["key_part"] = KeyPart.from_storage(metadata_dict["key_part"])
        class_instance.set_metadata_dict(metadata_dict)
        class_instance.fetch(directory_path)
        class_instance.copy_object_keys_from_metadata(metadata_dict)
        return class_instance

    def save(self, object_key: ObjectKey):
        directory_path = self.get_object_path(object_key)
        metadata_dict = self.get_metadata_dict()
        metadata_dict["key_part"] = metadata_dict["key_part"].to_storage()
        metadata_dict["class_name"] = self.get_class_name()
        self.copy_object_keys_to_metadata(metadata_dict)
        directory_path.ensure_exists()
        (directory_path // "metadata.json").put(metadata_dict)
        self.store(directory_path)

    def get_object_attribute_names(self):
        cls = self.get_class()
        marker_groups = Introspection.get_marker_groups(cls)
        object_keys = set(marker_groups.get("__objects__", {}).keys())
        return object_keys

    def copy_object_keys_to_metadata(self, metadata_dict):
        from agile_ai.memoization.object_option import ObjectOption
        object_names = self.get_object_attribute_names()
        for object_name in object_names:
            object_option: ObjectOption = getattr(self, object_name, ObjectOption.empty())
            if object_option.object_key is None:
                object_key = None
            else:
                object_key = object_option.object_key.to_storage()
            metadata_dict[object_name] = object_key

    def copy_object_keys_from_metadata(self, metadata_dict):
        from agile_ai.memoization.object_option import ObjectOption
        object_names = self.get_object_attribute_names()
        for object_name in object_names:
            value = metadata_dict[object_name]
            if value is None:
                object_option = ObjectOption.empty()
            else:
                object_key = ObjectKey.from_storage(value)
                object_option = ObjectOption(object_key)
            setattr(self, object_name, object_option)

    def get_object_path(self, object_key: Optional[ObjectKey] = None) -> DirectoryPath:
        from agile_ai.memoization.warehouse_service import WarehouseService
        warehouse_service = get_service(WarehouseService)
        if object_key is None:
           object_key = self.get_object_key()
        return warehouse_service.get_object_path(object_key)

    def fetch(self, directory_path):
        pass

    def store(self, directory_path):
        pass

    def allocate_storage(self: WarehouseObjectT) -> WarehouseObjectT:
        self.get_object_path().ensure_exists()
        return self

    def put(self: WarehouseObjectT) -> WarehouseObjectT:
        from agile_ai.memoization.object_option import ObjectOption
        ObjectOption(self).put()
        return self

    def configure(self, **kwargs):
        pass