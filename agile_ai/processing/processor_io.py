from agile_ai.memoization.warehouse_key import KeyTuple, KeyLiteral, ObjectKey
from agile_ai.memoization.warehouse_object import ObjectOption


class IO:
    def get_key(self) -> KeyTuple:
        key_list = []
        for field_name, key_type in self.__annotations__.items():
            key_value = getattr(self, field_name)
            print(field_name, key_type, key_value)
            if key_type in [str, int, float]:
                key = KeyLiteral(key_value)
            elif isinstance(key_value, ObjectKey):
                key = key_value
            elif isinstance(key_value, ObjectOption):
                key = key_value.object_or_key
            else:
                raise NotImplementedError(f"Unhandled key_type {key_type}")
            key_list.append(key)
        return KeyTuple(key_list)


