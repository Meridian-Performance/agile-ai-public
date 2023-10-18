from typing import TypeVar

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.decorators import get_service
from agile_ai.memoization.warehouse_key import ObjectKey, KeyPart
from agile_ai.processing.processor_io import ObjectWithOptions
from agile_ai.utilities.introspection import Introspection

WarehouseObjectT = TypeVar("WarehouseObjectT", bound="WarehouseObject")


class WarehouseObject(ObjectWithOptions):
    key_part: KeyPart

    def set_key_part(self, key_part: KeyPart):
        self.key_part = key_part
        return self

    def with_key_part(self, key_part: KeyPart):
        self.set_key_part(key_part)
        return self

    def __init__(self):
        self.key_part = None

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
        return self._copy_metadata(self.__dict__, destination_dict=dict())

    def set_metadata_dict(self, metadata_dict):
        self._copy_metadata(metadata_dict, self.__dict__)

    @classmethod
    def get_class(cls):
        return cls

    @classmethod
    def get_class_name(cls):
        return Introspection.get_class_name(cls)

    def get_object_key(self) -> ObjectKey:
        return ObjectKey(self.get_class(), self.key_part)

    @classmethod
    def load(cls, directory_path: DirectoryPath):
        metadata_dict = (directory_path // "metadata.json").get()
        metadata_dict["key_part"] = KeyPart.from_storage(metadata_dict["key_part"])
        class_instance = cls()
        class_instance.set_metadata_dict(metadata_dict)
        class_instance.fetch(directory_path)
        class_instance.copy_object_keys_from_metadata(metadata_dict)
        return class_instance

    def save(self, directory_path: DirectoryPath):
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
            object_option: ObjectOption = getattr(self, object_name)
            object_key = object_option.object_key.to_storage()
            metadata_dict[object_name] = object_key

    def copy_object_keys_from_metadata(self, metadata_dict):
        from agile_ai.memoization.object_option import ObjectOption
        object_names = self.get_object_attribute_names()
        for object_name in object_names:
            value = metadata_dict[object_name]
            object_key = ObjectKey.from_storage(value)
            object_option = ObjectOption(object_key)
            setattr(self, object_name, object_option)

    def get_object_path(self) -> DirectoryPath:
        from agile_ai.memoization.warehouse_service import WarehouseService
        warehouse_service = get_service(WarehouseService)
        return warehouse_service.get_object_path(self.get_object_key())

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