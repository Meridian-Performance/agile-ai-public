from typing import TypeVar, Generic, Iterator, Generator, Iterable

from agile_ai.memoization.object_option import ObjectOption, WarehouseObjectT
from agile_ai.memoization.warehouse_object import WarehouseObject

StreamElementT = TypeVar('StreamElementT')


class StreamOption(ObjectOption[WarehouseObjectT]):
    def get(self) -> WarehouseObjectT:
        return self._object_instance # warehouse_service.get_object(self.object_key)

class StreamObject(WarehouseObject, Generic[StreamElementT]):
    def stream(self) -> Iterator[StreamElementT]:
        yield from self.generator

    def set_generator(self, generator: Iterable[StreamElementT]):
        self.generator = generator
