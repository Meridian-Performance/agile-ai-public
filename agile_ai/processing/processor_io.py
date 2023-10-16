from typing import Type, Optional

from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyTuple, KeyLiteral, ObjectKey, KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.utilities.introspection import Introspection


class IO:
    def __init__(self):
        self.key_part = None

    def get_items(self):
        for field_name, key_type in Introspection.get_annotation_items(self):
            key_value = getattr(self, field_name)
            yield field_name, key_type, key_value

    def get_key(self) -> Optional[KeyTuple]:
        key_list = []
        for field_name, key_type, key_value in self.get_items():
            if key_type in [str, int, float]:
                key = KeyLiteral(key_value)
            elif isinstance(key_value, ObjectKey):
                key = key_value
            elif isinstance(key_value, ObjectOption):
                key = key_value.object_key
            else:
                return None
                # raise NotImplementedError(f"Unhandled key_type {key_type}")
            key_list.append(key)
        return KeyTuple(key_list)

    def all_options_present(self) -> bool:
        if self.key_part is None:
            return False
        for field_name, key_type, key_value in self.get_items():
            if isinstance(key_value, ObjectOption):
                if key_value.is_empty():
                    return False
        return True

    def store_options(self):
        for field_name, key_type, key_value in self.get_items():
            if isinstance(key_value, ObjectOption):
                if not key_value.is_set():
                    raise ValueError(f"Output `{field_name}` ObjectOption of type `{key_type.__args__[0]}` is empty")
                key_value.put()

    def init_options(self, key_part: KeyPart):
        self.key_part = key_part
        for field_name, key_type in Introspection.get_annotation_items(self):
            if "ObjectOption" in str(key_type):
                object_cls: Type[WarehouseObject] = key_type.__args__[0]
                object_instance = object_cls().with_key_part(key_part)
                key_value = ObjectOption(object_instance)
                setattr(self, field_name, key_value)

