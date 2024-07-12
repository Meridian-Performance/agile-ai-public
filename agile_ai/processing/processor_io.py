from typing import Type, Optional, TypeVar

from agile_ai.memoization.warehouse_key import KeyTuple, KeyLiteral, ObjectKey, KeyPart, ExcludedKey
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

    def all_options_present(self, status_log=False) -> bool:
        for field_name, key_type, key_value in self.get_object_options():
            if key_value.is_empty():
                if status_log:
                    print(f"  All options present check: field `{field_name}` of type `{key_type}` is empty")
                return False
        return True

    def store_options(self):
        for field_name, key_type, key_value in self.get_object_options():
            key_value.assert_set(field_name, key_type)
            key_value.put()
        return self

    def init_options(self: T, key_part: Optional[KeyPart] = None) -> T:
        for field_name, key_type in Introspection.get_annotation_items(self):
            ObjectOptionCls = Introspection.get_object_option_cls(key_type)
            if ObjectOptionCls:
                from agile_ai.memoization.warehouse_object import WarehouseObject
                object_cls: Type[WarehouseObject] = key_type.__args__[0]
                object_instance = object_cls().with_key_part(key_part)
                key_value = ObjectOptionCls(object_instance)
                setattr(self, field_name, key_value)
        return self


class IO(ObjectWithOptions):
    def __init__(self):
        self.key_part = None

    def get_key(self) -> Optional[KeyTuple]:
        key_list = []
        for field_name, key_type, key_value in self.get_items():
            if key_type in [str, int, float, bool]:
                key = KeyLiteral(key_value)
            elif isinstance(key_value, ObjectKey):
                key = key_value
            elif Introspection.is_object_option(key_value):
                key = key_value.object_key
            elif Introspection.is_union(key_type):
                union_types = Introspection.get_union_types(key_type)
                if ExcludedKey in union_types:
                    continue
                if str in union_types:
                    key = KeyLiteral(str(key_value))
                else:
                    print(f"Warning, unhandled key_type {key_type} excluded from key list")
                    continue
            else:
                print(f"Warning, unhandled key_type {key_type} excluded from key list")
                continue
            key_list.append(key)
        return KeyTuple(key_list)

    def all_options_present(self, status_log=False) -> bool:
        if self.key_part is None:
            if status_log:
                print("  All options present check: Key part is not sent")
            return False
        return ObjectWithOptions.all_options_present(self, status_log=status_log)

    def init_options(self, key_part: Optional[KeyPart] = None):
        self.key_part = key_part
        ObjectWithOptions.init_options(self, key_part)
