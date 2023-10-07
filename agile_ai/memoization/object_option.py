from typing import Generic, Union, Type, Optional

from agile_ai.injection.decorators import autowire
from agile_ai.memoization.warehouse_key import WarehouseObjectT, ObjectKey, KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import WarehouseService


class ObjectOption(Generic[WarehouseObjectT]):
    warehouse_service: WarehouseService = autowire(WarehouseService)
    object_key: ObjectKey
    object_instance: Optional[WarehouseObject]

    def __init__(self, object_or_key: Union[WarehouseObject, ObjectKey]):
        self.object_or_key = object_or_key
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

    def set(self, object_instance: WarehouseObjectT):
        self.object_instance = object_instance

    def put(self):
        self.warehouse_service.put_object(self.object_instance)