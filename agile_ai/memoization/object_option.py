from typing import Generic, Union, Type, Optional, TypeVar

from agile_ai.injection.decorators import get_service
from agile_ai.memoization.warehouse_key import ObjectKey, KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject

WarehouseObjectT = TypeVar("WarehouseObjectT", bound=WarehouseObject)


class ObjectOption(Generic[WarehouseObjectT]):
    """
        An ObjectOption is only considered present if saved to disk

        If it "is_set", it can be saved to disk
        "put" saves it to disk.
    """
    object_key: ObjectKey
    _object_instance: Optional[WarehouseObjectT]

    def __init__(self, object_or_key: Union[WarehouseObject, ObjectKey]):
        from agile_ai.memoization.warehouse_service import WarehouseService
        self.warehouse_service = get_service(WarehouseService)
        if isinstance(object_or_key, ObjectKey):
            self._set_object_key(object_or_key)
        if isinstance(object_or_key, WarehouseObject):
            self._set_warehouse_object(object_or_key)

    def _set_object_key(self, object_key: ObjectKey):
        self.object_key = object_key
        self._object_instance = None

    def _set_warehouse_object(self, warehouse_object: WarehouseObject):
        self.object_key = warehouse_object.get_object_key()
        self._object_instance = warehouse_object

    def __call__(self, object_instance: Optional[WarehouseObjectT] = None, **kwargs) -> Optional[WarehouseObjectT]:
        if self._object_instance is None:
            object_class = self.object_key.get_class()
            object_instance = object_class()
        if object_instance:
            self._set_warehouse_object(object_instance)
        self._object_instance.configure(**kwargs)
        return self._object_instance

    @staticmethod
    def Key(object_cls: Type[WarehouseObjectT], key_part: KeyPart):
        object_key = ObjectKey[WarehouseObjectT](object_cls, key_part)
        return ObjectOption[WarehouseObjectT](object_key)

    def is_present(self) -> bool:
        if self.object_key is None:
            return False
        return self.warehouse_service.has_object(self.object_key)

    def is_empty(self) -> bool:
        return not self.is_present()

    def get(self) -> WarehouseObjectT:
        return self.warehouse_service.get_object(self.object_key)

    def assert_set(self, field_name: str, key_type):
        base_str = f"ObjectOption `{field_name}` of type `{key_type.__args__[0]}`, it isn't considered 'set'"
        if not self._object_instance:
            raise ValueError(f"{base_str}: object instance is None")
        if not self.object_key:
            raise ValueError(f"{base_str}: object key is None")
        if not self.object_key.key_part:
            raise ValueError(f"{base_str}: object key part is None")

    def put(self):
        self.warehouse_service.put_object(self._object_instance)
        return self

    @classmethod
    def empty(cls):
        empty_option = ObjectOption(None)
        empty_option.object_key = None
        return empty_option