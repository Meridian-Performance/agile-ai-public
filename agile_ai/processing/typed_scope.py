from typing import TypeVar, Generic

T = TypeVar('T')


class TypedScopeContainer(Generic[T]):
    def __call__(self, typed_object: T):
        self.typed_object = typed_object

    def __enter__(self) -> T:
        return self.typed_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True;


class TypedScope(Generic[T]):
    def __init__(self: T):
        pass

    def __enter__(self) -> T:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True
