from typing import Callable, Tuple, Generator, Iterator

import numpy as np

from agile_ai.injection.decorators import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import WarehouseService
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai.processing.stream_object import StreamObject, StreamOption
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, describe, it, fit, with_stubs
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import attach_stub
from pynetest.test_doubles.stub import MegaStub
from numpy.typing import NDArray


class TestContext(TCBase):
    __services__: Marker
    warehouse_service: WarehouseService

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


class SomeStreamA(StreamObject[NDArray]):
    pass


class SomeStreamB(StreamObject):
    pass


class StreamProcessorA(Processor):
    class Inputs(IO):
        array_count: int
        array_size: int

    class Outputs(IO):
        some_stream_a: StreamOption[SomeStreamA]

    def perform(self, inputs: Inputs, outputs: Outputs):
        some_stream_a = outputs.some_stream_a()
        some_stream_a.set_generator(self.generate_arrays(inputs))

    def generate_arrays(self, inputs) -> Iterator[NDArray]:
        for i in range(inputs.array_count):
            yield np.full((inputs.array_size, inputs.array_size), i, dtype=int)

    inputs: Inputs
    resolve: Callable[..., Outputs]


class StreamProcessorB(Processor):
    memoize: bool

    class Inputs(IO):
        skip: int
        some_stream_a: StreamOption[SomeStreamA]

    class Outputs(IO):
        some_stream_b: StreamOption[SomeStreamB]

    def perform(self, inputs: Inputs, outputs: Outputs):
        some_stream_b = outputs.some_stream_b(memoize=self.memoize)
        some_stream_b.set_generator(self.generate_arrays(inputs))

    def generate_arrays(self, inputs) -> Iterator[NDArray]:
        for array in inputs.some_stream_a.get().stream():
            yield self.process_element(inputs.skip, array)

    def process_element(self, skip: int, array: NDArray) -> NDArray:
        return array[::skip, ::skip]

    inputs: Inputs
    resolve: Callable[..., Outputs]


def get_processors() -> StreamProcessorB:
    stream_processor_a = StreamProcessorA()
    stream_processor_a.inputs.array_count = 10
    stream_processor_a.inputs.array_size = 20
    stream_processor_b = StreamProcessorB()
    stream_processor_b.inputs.some_stream_a = stream_processor_a.resolve().some_stream_a
    stream_processor_b.inputs.skip = 2
    return stream_processor_b


@pyne
def stream_processor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.warehouse_service.set_warehouse_directory(tc.test_directory / "warehouse")
        tc.warehouse_service.set_partition_name("some_partition_name")
        tc.warehouse_service.register_object_class(SomeStreamA)
        tc.warehouse_service.register_object_class(SomeStreamB)

    @it("creates an iterable output stream object")
    def _(tc: TestContext):
        stream_processor_b = get_processors()
        stream_processor_b.memoize = False
        some_stream_b = stream_processor_b.resolve().some_stream_b.get()
        array_list = list(some_stream_b.stream())
        expect(array_list).to_have_length(10)
        expect(array_list[-1].shape).to_be((10, 10))
        expect(array_list[9][0, 0]).to_be(9)

    @describe("when the processors are configured to not memoize the streams")
    def _():
        @describe("when the object is streamed")
        def _():
            @it("doesn't create any warehouse objects")
            def _(tc: TestContext):
                stream_processor_b = get_processors()
                stream_processor_b.memoize = False
                some_stream_b_option = stream_processor_b.resolve().some_stream_b
                list(some_stream_b_option.get().stream())
                expect(some_stream_b_option.is_present()).to_be(False)

    @describe("when the processors are configured to memoize the streams")
    def _():
        @describe("when the object is streamed")
        def _():
            @it("creates a warehouse object")
            def _(tc: TestContext):
                stream_processor_b = get_processors()
                stream_processor_b.memoize = True
                some_stream_b_option = stream_processor_b.resolve().some_stream_b
                some_stream_b_option.get().consume()
                expect(some_stream_b_option.is_present()).to_be(True)

        @describe("streamed a second time")
        def _():
            @before_each
            def _(tc: TestContext):
                stream_processor_b = get_processors()
                stream_processor_b.memoize = True
                some_stream_b = stream_processor_b.resolve().some_stream_b.get()
                some_stream_b.consume()
                tc.stubs = attach_stub(StreamProcessorB, "process_element").then_return(None)
            @it("uses the memoization")
            @with_stubs
            def _(tc: TestContext):
                stream_processor_b = get_processors()
                stream_processor_b.memoize = True
                some_stream_b = stream_processor_b.resolve().some_stream_b.get()
                list(some_stream_b.stream())
                expect(StreamProcessorB.process_element).was_not_called()