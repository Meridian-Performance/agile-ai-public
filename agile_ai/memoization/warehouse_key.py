from hashlib import md5
from typing import Type, List, Tuple, Union

import numpy as np

from agile_ai.utilities.introspection import Introspection
from agile_ai.utilities.option import Option

WarehouseObject = "agile_ai.memoization.warehouse_object.WarehouseObject"


def compute_md5_hex(values):
    md5_hash = md5()
    for value in values:
        if isinstance(value, Option):
            if value.is_empty():
                continue
            value = value.get()
        if isinstance(value, np.ndarray):
            if value is not None:
                value = value.tobytes()
        if isinstance(value, int):
            value = str(value)
        if isinstance(value, float):
            value = str(value)
        if isinstance(value, str):
            value = value.encode("utf-8")
        try:
            if value is not None:
                md5_hash.update(value)
        except TypeError as e:
            raise TypeError(f"Unable to add {value} to the md5_hex \n {e}")
    return md5_hash.hexdigest()


class KeyPart:
    def get_storage_string(self):
        raise NotImplementedError

    @classmethod
    def from_storage(cls, value: Union[list, str]):
        if isinstance(value, list):
            return KeyTuple.from_storage(value)
        if isinstance(value, str):
            return KeyLiteral.from_storage(value)

    def to_storage(self) -> Tuple:
        raise NotImplementedError


class KeyLiteral(KeyPart):
    def __init__(self, key_string: str):
        self.key_string = key_string

    def get_storage_string(self):
        return compute_md5_hex(self.key_string)

    @classmethod
    def from_storage(cls, value: str):
        return KeyLiteral(value)

    def to_storage(self) -> str:
        return self.key_string


class KeyTuple(KeyPart):

    def __init__(self, key_parts: List[KeyPart]):
        self.key_parts = key_parts

    def get_storage_string(self):
        values = [kp.get_storage_string() for kp in self.key_parts]
        return compute_md5_hex(values)

    @classmethod
    def from_storage(cls, values: list):
        key_parts = [KeyPart.from_storage(value) for value in values]
        return KeyTuple(key_parts)

    def to_storage(self) -> List:
        return [key_part.to_storage() for key_part in self.key_parts]


def _standardize_key_part(key_part: Union[KeyPart, str]) -> KeyPart:
    if isinstance(key_part, str):
        return KeyLiteral(key_part)
    elif isinstance(key_part, KeyTuple):
        return key_part
    else:
        raise NotImplementedError(f"Unable to convert {key_part} to a KeyPart")


def key(key_parts: List["KeyPart"]) -> KeyTuple:
    key_parts = [_standardize_key_part(kp) for kp in key_parts]
    return KeyTuple(key_parts)


class ObjectKey(KeyPart):
    object_cls: Type[WarehouseObject]
    key_part: KeyPart

    def __init__(self, object_cls: Type[WarehouseObject], key_part: KeyPart):
        self.object_cls = object_cls
        self.key_part = key_part

    def get_storage_string(self):
        return self.get_key_tuple().get_storage_string()

    def get_key_part(self) -> KeyPart:
        return self.key_part

    def get_key_tuple(self) -> KeyTuple:
        return KeyTuple([self.get_class_key(), self.key_part])

    def get_class_key(self) -> KeyPart:
        return KeyLiteral(self.get_class_name())

    def get_class_name(self) -> str:
        return Introspection.get_class_name(self.object_cls)

    def get_class(self) -> Type[WarehouseObject]:
        return self.object_cls

    @classmethod
    def from_tuple(cls, key_parts_tuple):
        pass
