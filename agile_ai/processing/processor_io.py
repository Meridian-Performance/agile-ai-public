from typing import Type

from agile_ai.memoization.warehouse_key import KeyTuple, KeyLiteral, ObjectKey, KeyPart
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_object import WarehouseObject


class IO:

    def get_items(self):
        for field_name, key_type in self.__annotations__.items():
            key_value = getattr(self, field_name)
            yield field_name, key_type, key_value

    def get_key(self) -> KeyTuple:
        key_list = []
        for field_name, key_type, key_value in self.get_items():
            if key_type in [str, int, float]:
                key = KeyLiteral(key_value)
            elif isinstance(key_value, ObjectKey):
                key = key_value
            elif isinstance(key_value, ObjectOption):
                key = key_value.object_key
            else:
                raise NotImplementedError(f"Unhandled key_type {key_type}")
            key_list.append(key)
        return KeyTuple(key_list)

    def all_options_present(self) -> bool:
        for field_name, key_type, key_value in self.get_items():
            if isinstance(key_value, ObjectOption):
                if key_value.is_empty():
                    return False
        return True

    def store_options(self):
        for field_name, key_type, key_value in self.get_items():
            if isinstance(key_value, ObjectOption):
                key_value.put()

    def init_options(self, key_part: KeyPart):
        for field_name, key_type in self.__annotations__.items():
            if "ObjectOption" in str(key_type):
                object_cls: Type[WarehouseObject] = key_type.__args__[0]
                key_value = ObjectOption(object_cls().with_key_part(key_part))
                setattr(self, field_name, key_value)

