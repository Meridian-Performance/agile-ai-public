from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.memoization.warehouse_key import ObjectKey, KeyPart
from agile_ai.utilities.introspection import Introspection


class WarehouseObject:
    key_part: KeyPart

    def set_key_part(self, key_part: KeyPart):
        self.key_part = key_part

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
            if metadata_value:
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
        return class_instance

    def save(self, directory_path: DirectoryPath):
        metadata_dict = self.get_metadata_dict()
        metadata_dict["key_part"] = metadata_dict["key_part"].to_storage()
        metadata_dict["class_name"] = self.get_class_name()
        directory_path.ensure_exists()
        (directory_path // "metadata.json").put(metadata_dict)
        self.store(directory_path)

    def fetch(self, directory_path):
        pass

    def store(self, directory_path):
        pass


