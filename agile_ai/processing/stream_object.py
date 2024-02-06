from typing import TypeVar, Generic, Iterator, Generator, Iterable, Optional

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.injection.decorators import autowire
from agile_ai.memoization.object_option import ObjectOption, WarehouseObjectT
from agile_ai.memoization.warehouse_key import KeyPart
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import WarehouseService, register_object_class

StreamElementT = TypeVar('StreamElementT')


class StreamObject(WarehouseObject, Generic[StreamElementT]):
    generator: Iterable[StreamElementT]
    warehouse_service: WarehouseService = autowire(WarehouseService)
    memoize: bool

    __metadata__: Marker
    count: int
    extension: str

    def __init__(self, key_part: Optional[KeyPart] = None, partition_name: Optional[str] = None):
        super().__init__(key_part, partition_name)
        self.generator = None
        self.memoize = True
        self.extension = self.get_extension()
        self.count = -1

    @classmethod
    def get_extension(cls):
        return "pkl"

    def consume(self):
        for element in self.stream():
            pass

    def stream(self) -> Iterator[StreamElementT]:
        if self.memoize:
            if self.count != -1:
                yield from self.stream_from_storage()
            else:
                index = -1
                for index, element in enumerate(self.generator):
                    if element is None:
                        yield None
                    else:
                        yield self.put_element(index, element)
                self.count = index + 1
                self.warehouse_service.put_object(self)
        else:
            yield from self.generator

    def stream_from_storage(self) -> Iterator[StreamElementT]:
        for index in range(self.count):
            yield self.get_element(index)

    def put_element(self, index: int, element: StreamElementT) -> StreamElementT:
        self.get_element_path(index).put(element)
        return element

    def get_element(self, index: int, check=False) -> StreamElementT:
        path = self.get_element_path(index)
        if check and not path.exists():
            return None
        return path.get()

    def set_generator(self, generator: Iterable[StreamElementT]):
        self.generator = generator

    def configure(self, memoize: bool = False, extension: str = None):
        self.memoize = memoize
        if extension:
            self.extension = extension;

    def get_element_path(self, index: int) -> FilePath:
        return self.get_object_path() // f"element_{index:06d}.{self.extension}"


register_object_class(StreamObject)


class StreamOption(ObjectOption[WarehouseObjectT]):
    def get(self) -> WarehouseObjectT:
        object_instance: StreamObject = self._object_instance
        if self.warehouse_service.has_object(self.object_key):
            return self.warehouse_service.get_object(self.object_key)
        return object_instance

    def put(self):
        return self
