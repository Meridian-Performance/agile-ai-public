from typing import Type, Optional, TypeVar

from agile_ai.memoization.warehouse_key import KeyTuple, KeyLiteral, ObjectKey, KeyPart
from agile_ai.utilities.introspection import Introspection

T = TypeVar("T")


class ObjectWithOptions:
    def get_items(self):
        for field_name, key_type in Introspection.get_annotation_items(self):
            key_value = getattr(self, field_name)
            yield field_name, key_type, key_value

    def get_object_options(self):
        for field_name, key_type in Introspection.get_annotation_items(self):
            if Introspection.is_object_option_cls(key_type):
                key_value = getattr(self, field_name)
                yield field_name, key_type, key_value

    def has_options(self):
        for field_name, key_type, key_value in self.get_object_options():
            return True
        return False

    def all_options_present(self) -> bool:
        for field_name, key_type, key_value in self.get_object_options():
            if key_value.is_empty():
                return False
        return True

    def store_options(self):
        for field_name, key_type, key_value in self.get_object_options():
            key_value.assert_set(field_name, key_type)
            key_value.put()
        return self

    def init_options(self: T, key_part: Optional[KeyPart] = None) -> T:
        for field_name, key_type in Introspection.get_annotation_items(self):
            if "ObjectOption" in str(key_type):
                from agile_ai.memoization.warehouse_object import WarehouseObject
                object_cls: Type[WarehouseObject] = key_type.__args__[0]
                object_instance = object_cls().with_key_part(key_part)
                from agile_ai.memoization.object_option import ObjectOption
                key_value = ObjectOption(object_instance)
                setattr(self, field_name, key_value)
        return self


class IO(ObjectWithOptions):
    def __init__(self):
        self.key_part = None

    def get_key(self) -> Optional[KeyTuple]:
        key_list = []
        for field_name, key_type, key_value in self.get_items():
            if key_type in [str, int, float]:
                key = KeyLiteral(key_value)
            elif isinstance(key_value, ObjectKey):
                key = key_value
            elif Introspection.is_object_option(key_value):
                key = key_value.object_key
            else:
                return None
                # raise NotImplementedError(f"Unhandled key_type {key_type}")
            key_list.append(key)
        return KeyTuple(key_list)

    def all_options_present(self) -> bool:
        if self.key_part is None:
            return False
        return ObjectWithOptions.all_options_present(self)

    def init_options(self, key_part: Optional[KeyPart] = None):
        self.key_part = key_part
        ObjectWithOptions.init_options(self, key_part)
