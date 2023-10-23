from hashlib import md5
from typing import Type, List, Tuple, Union, TypeVar, Generic, Optional

import numpy as np

from agile_ai.utilities.introspection import Introspection
from agile_ai.utilities.option import Option

WarehouseObjectAlias = "agile_ai.memoization.warehouse_object.WarehouseObject"


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
    def from_storage(cls, value: Union[str, Tuple]):
        if isinstance(value, tuple):
            return KeyTuple([KeyPart.from_storage(item) for item in value])
        if isinstance(value, list):
            return ObjectKey.from_storage(value)
        if value.startswith("["):
            return ObjectKey.from_storage(value)
        if value.startswith("("):
            return KeyTuple.from_storage(value)
        return KeyLiteral.from_storage(value)

    def to_storage(self) -> str:
        raise NotImplementedError


class KeyLiteral(KeyPart):
    def __init__(self, literal: Union[str, int, float]):
        self.literal = literal

    def get_storage_string(self):
        return compute_md5_hex(str(self.literal))

    @classmethod
    def from_storage(cls, literal: str):
        if literal.startswith('"'):
            literal = literal[1:-1]
        if literal.startswith("int:"):
            literal = int(literal[4:])
        elif literal.startswith("float:"):
            literal = float(literal[6:])
        return KeyLiteral(literal)

    def to_storage(self) -> str:
        literal_type = None
        if isinstance(self.literal, int):
            literal_type = "int"
        if isinstance(self.literal, float):
            literal_type = "float"
        if literal_type:
            return f'"{literal_type}:{self.literal}"'
        return f'"{self.literal}"'

    def __eq__(self, other):
        if not isinstance(other, KeyLiteral):
            return False
        return self.literal == other.literal

    def __repr__(self):
        return f'KeyLiteral<{self.literal}>'


class KeyTuple(KeyPart):

    def __init__(self, key_parts: List[KeyPart]):
        for key_part in key_parts:
            if not isinstance(key_part, KeyPart):
                raise TypeError(f"key_part `{key_part}` is not actually a KeyPart")
        self.key_parts = key_parts

    def get_storage_string(self):
        values = [kp.get_storage_string() for kp in self.key_parts]
        return compute_md5_hex(values)

    @classmethod
    def from_storage(cls, values: str) -> "KeyTuple":
        items = np.safe_eval(values)
        items = [KeyPart.from_storage(item) for item in items]
        return KeyTuple(items)

    def to_storage(self) -> str:
        storage_strings = [key_part.to_storage() for key_part in self.key_parts]
        if len(storage_strings) == 1:
            storage_strings.append("")

        return "(" + ", ".join(storage_strings) + ")"


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


WarehouseObjectT = TypeVar("WarehouseObjectT", bound=WarehouseObjectAlias)

T = TypeVar("T")

class ObjectKey(Generic[WarehouseObjectT], KeyPart):
    object_cls: Type[WarehouseObjectAlias]
    key_part: KeyPart
    object_cls_name: str
    partition_name: Optional[str]

    def __init__(self, object_cls: Type[WarehouseObjectAlias], key_part: KeyPart, object_cls_name=None, partition_name: Optional[str]=None):
        self.object_cls = object_cls
        if not object_cls_name:
            object_cls_name = Introspection.get_class_name(object_cls)
        self.object_cls_name = object_cls_name
        self.key_part = key_part
        self.partition_name = partition_name

    def copy(self: Type[T], partition_name: Optional[str] = None, key_part: Optional[KeyPart] = None) -> T:
        key_copy = ObjectKey(object_cls=self.object_cls,
                             object_cls_name=self.object_cls_name,
                             key_part=self.key_part,
                             partition_name=self.partition_name
                             )
        if partition_name:
            key_copy.partition_name = partition_name
        if key_part:
            key_copy.key_part = key_part
        return key_copy


    def get_storage_string(self):
        return self.get_key_tuple().get_storage_string()

    def get_key_part(self) -> KeyPart:
        return self.key_part

    def get_key_tuple(self) -> KeyTuple:
        if self.key_part is None:
            raise ValueError(f"ObjectKey<{self.object_cls_name}> key_part is None, did you forget to set it?")
        return KeyTuple([self.get_class_key(), self.key_part])

    def get_class_key(self) -> KeyPart:
        return KeyLiteral(self.object_cls_name)

    def get_class(self) -> Type[WarehouseObjectAlias]:
        return self.object_cls

    def to_storage(self) -> str:
        return f'["{self.object_cls_name}", {self.key_part.to_storage()}]'

    @classmethod
    def from_storage(cls, value: Union[str, List]):
        if isinstance(value, str):
            items = np.safe_eval(value)
            return KeyPart.from_storage(items)
        object_cls_name, key_part = value
        key_part = KeyPart.from_storage(key_part)
        return ObjectKey(object_cls=None, key_part=key_part, object_cls_name=object_cls_name)

    def __eq__(self, other):
        if not isinstance(other, ObjectKey):
            return False
        return self.to_storage() == other.to_storage()

    def with_partition_name(self, partition_name: str):
        if partition_name:
            self.partition_name = partition_name
        return self

    def __repr__(self):
        return f'ObjectKey<{self.get_storage_string()}>'

    def __str__(self):
        return repr(self)


class StorageKey(KeyPart):
    def __init__(self, md5_hex: str):
        self.md5_hex = md5_hex

    def get_storage_string(self):
        return self.md5_hex

    @classmethod
    def from_storage(cls, md5_hex: str):
        raise NotImplementedError

    def to_storage(self) -> str:
        return f'"{self.md5_hex}"'

    def __eq__(self, other):
        if not isinstance(other, StorageKey):
            return False
        return self.md5_hex == other.md5_hex

    def __repr__(self):
        return f'StorageKey<{self.md5_hex}>'

    def __str__(self):
        return repr(self)
