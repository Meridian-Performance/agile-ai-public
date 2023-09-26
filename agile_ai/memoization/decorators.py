from typing import TypeVar, Callable

TypedCallable = TypeVar("TypedCallable", bound=Callable)



def self_memo(fun: TypedCallable) -> TypedCallable:
    shadow_name = "__memo_for_" + fun.__name__

    def inner_fun(self, *args, **kwargs):
        if hasattr(self, shadow_name):
            return getattr(self, shadow_name)
        value = fun(self, *args, **kwargs)
        setattr(self, shadow_name, value)
        return value
    return inner_fun


def self_last_args_memo(fun: TypedCallable) -> TypedCallable:
    shadow_name = "__memo_last_args_for_" + fun.__name__

    def inner_fun(self, *args, **kwargs):
        if hasattr(self, shadow_name):
            last_args, last_kwargs, last_value = getattr(self, shadow_name)
            if last_args == args and last_kwargs == kwargs:
                return last_value
        value = fun(self, *args, **kwargs)
        setattr(self, shadow_name, (args, kwargs, value))
        return value
    return inner_fun


def self_memo_property(fun):
    shadow_name = "__memo_for_" + fun.__name__

    def getter(self, *args, **kwargs):
        if hasattr(self, shadow_name):
            return getattr(self, shadow_name)
        value = fun(self, *args, **kwargs)
        setattr(self, shadow_name, value)
        return value

    def setter(self, value):
        setattr(self, shadow_name, value)

    return property(fget=getter, fset=setter)


def fun_memo(fun):
    fun.memo = None

    def inner_fun(*args, **kwargs):
        if fun.memo is not None:
            return fun.memo
        value = fun(*args, **kwargs)
        fun.memo = value
        return value

    return inner_fun


def all_args_constructor(cls):
    if '__annotations__' in cls.__dict__:
        constructor_args = list(cls.__dict__['__annotations__'].keys())

        def all_args_init(self, *args, **kwargs):
            if args:
                raise ValueError("Only keywords allowed in all args constructor")
            for k in constructor_args:
                setattr(self, k, None)
            for k, v in kwargs.items():
                setattr(self, k, v)

        cls.__init__ = all_args_init
        return cls
    else:
        raise ValueError(f"Class {cls} has no annotations")


def file_memo(file_path):
    def memoize_file(fun):
        def inner(*args, **kwargs):
            if file_path.exists():
                return file_path.get()
            else:
                result = fun(*args, **kwargs)
                file_path.put(result)
                return result
        return inner
    return memoize_file
