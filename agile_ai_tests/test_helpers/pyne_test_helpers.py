import types
from typing import Optional, Iterable

from agile_ai.injection.decorators import autowire_services
from pynetest.pyne_test_collector import before_each as old_before_each
from pynetest.pyne_test_collector import describe as old_describe
from pynetest.pyne_test_collector import fdescribe as old_fdescribe
from pynetest.pyne_test_collector import fit as old_fit
from pynetest.pyne_test_collector import it as old_it
from pynetest.pyne_test_collector import xdescribe as old_xdescribe
from pynetest.pyne_test_collector import xit as old_xit

from agile_ai.data_marshalling.directory_path import DirectoryPath
from libraries.pynetest.test_doubles.stub import MegaStub

describe = old_describe
xdescribe = old_xdescribe
fdescribe = old_fdescribe


def with_new_test_context(TestContext):
    def decorator(fun):
        test_context = TestContext()

        def wrapped_fun(self):
            self.test_context = test_context
            return fun(test_context)

        return wrapped_fun

    return decorator


def with_test_context(fun):
    def wrapped_fun(self):
        return fun(self.test_context)
    return wrapped_fun


def wrap_old_it(old_it):
    def new_it(text):
        def wrapper(fun):
            return old_it(text)(with_test_context(fun))

        return wrapper

    new_it.__name__ = old_it.__name__
    return new_it


it = wrap_old_it(old_it)
fit = wrap_old_it(old_fit)
xit = wrap_old_it(old_xit)


def _wrap_with_stubs(fun, stubs_name):
    def wrapper(tc):
        stubs = getattr(tc, stubs_name)
        with stubs:
            fun(tc)
    return wrapper


def _wrap_with_test_context(fun, new_test_context_cls: Optional):
    def wrapper(context):
        if new_test_context_cls:
            context.test_context = new_test_context_cls()
        if not hasattr(context, "test_context"):
            raise AttributeError("No 'test_context' exists on pyne's 'self' test context.\n"
                                 "Try initializing a TestContext in the new-style before_each\n"
                                 "E.g. @before_each(TestContext)\n"
                                 )
        test_context = context.test_context
        return fun(test_context)
    return old_before_each(wrapper)


def with_stubs(stubs_name_or_fun):
    # This may be called as a function with an alternative stub name to yield a decorator
    # Or just used as a decorator
    if isinstance(stubs_name_or_fun, str):
        return lambda fun: _wrap_with_stubs(fun=fun, stubs_name=stubs_name_or_fun)
    else:
        return _wrap_with_stubs(fun=stubs_name_or_fun, stubs_name="stubs")


def before_each(test_context_cls_or_fun):
    # This may be called as a function with a test_context to yield a decorator
    # Or just used as a decorator
    if isinstance(test_context_cls_or_fun, types.FunctionType):
        fun = test_context_cls_or_fun
        return _wrap_with_test_context(fun=fun, new_test_context_cls=None)
    else:
        test_context_cls = test_context_cls_or_fun
        return lambda fun: _wrap_with_test_context(fun=fun, new_test_context_cls=test_context_cls)


def function_that_returns_values(values: Iterable):
    values_iter = iter(values)

    def wrapped_function(*args, **kwargs):
        return next(values_iter)

    return wrapped_function


class TCBase:
    stubs: MegaStub

    @property
    def test_directory(self) -> DirectoryPath:
        pass

    @classmethod
    def initialize_services(cls):
        autowire_services(cls)

    @property
    def test_directory(self) -> DirectoryPath:
        return self.test_directory_service.test_directory

    def __init__(self):
        self.initialize_services()
