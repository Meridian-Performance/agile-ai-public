from typing import Generic, Union, Type, Optional, TypeVar

from agile_ai.injection.decorators import autowire, get_service
from agile_ai.memoization.warehouse_key import ObjectKey, KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject

WarehouseObjectT = TypeVar("WarehouseObjectT", bound=WarehouseObject)


class ObjectOption(Generic[WarehouseObjectT]):
    object_key: ObjectKey
    object_instance: Optional[WarehouseObjectT]

    def __init__(self, object_or_key: Union[WarehouseObject, ObjectKey]):
        from agile_ai.memoization.warehouse_service import WarehouseService
        self.warehouse_service = get_service(WarehouseService)
        if isinstance(object_or_key, ObjectKey):
            self.object_key = object_or_key
            self.object_instance = None
        if isinstance(object_or_key, WarehouseObject):
            self.object_key = object_or_key.get_object_key()
            self.object_instance = object_or_key

    @staticmethod
    def Key(object_cls: Type[WarehouseObjectT], key_part: KeyPart):
        object_key = ObjectKey[WarehouseObjectT](object_cls, key_part)
        return ObjectOption[WarehouseObjectT](object_key)

    def is_present(self) -> bool:
        return self.warehouse_service.has_object(self.object_key)

    def is_empty(self) -> bool:
        return not self.is_present()

    def get(self) -> WarehouseObjectT:
        return self.warehouse_service.get_object(self.object_key)

    def is_set(self) -> bool:
        if not self.object_instance:
            return False
        if not self.object_key:
            return False
        if not self.object_key.key_part:
            return False
        return True

    def put(self):
        self.warehouse_service.put_object(self.object_instance)
