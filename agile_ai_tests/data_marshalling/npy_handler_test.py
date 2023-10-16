from pathlib import Path

import numpy as np

from agile_ai.data_marshalling.npy_handler import NpyHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import exactly_equal_to_array, an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    array: np.ndarray
    path: Path


@pyne
def numpy_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.array = np.arange(0, 100, dtype=int)
        tc.path = tc.test_directory // "test.npy"

    @describe("#load")
    def _():
        @before_each
        def _(tc: TestContext):
            np.save(str(tc.path), tc.array)

        @it("loads the numpy array")
        def _(tc: TestContext):
            array = NpyHandler.load(tc.path)
            expect(array).to_be_a(np.ndarray)
            expect(array).to_have_length(100)
            expect(array).to_be(exactly_equal_to_array(tc.array))
            expect(array.flags.owndata).to_be(True)

        @describe("when loaded as a read-only memory map")
        def _():
            @it("loads the numpy array as a read-only memory map")
            def _(tc: TestContext):
                array = NpyHandler.load(tc.path, read_only_memmap=True)
                expect(array).to_be_a(np.ndarray)
                expect(array).to_have_length(100)
                expect(array).to_be(exactly_equal_to_array(tc.array))
                expect(array.flags.owndata).to_be(False)
                expect(array.flags.writeable).to_be(False)

        @describe("when loaded as a read-write memory map")
        def _():
            @it("loads the numpy array as a read-write memory map, writing changes to desk")
            def _(tc: TestContext):
                array = NpyHandler.load(str(tc.path), read_write_memmap=True)
                expect(array).to_be_a(np.ndarray)
                expect(array).to_have_length(100)
                expect(array).to_be(exactly_equal_to_array(tc.array))
                expect(array.flags.owndata).to_be(False)
                expect(array.flags.writeable).to_be(True)

                array[0] = 500

                reloaded_array = NpyHandler.load(tc.path)
                expect(reloaded_array[0]).to_be(500)

        @describe("when loaded as a read-copy memory map")
        def _():
            @it("loads the numpy array as a read-copy memory map, writing changes to memory, but not disk")
            def _(tc: TestContext):
                array = NpyHandler.load(tc.path, read_copy_memmap=True)
                expect(array).to_be_a(np.ndarray)
                expect(array).to_have_length(100)
                expect(array).to_be(exactly_equal_to_array(tc.array))
                expect(array.flags.owndata).to_be(False)
                expect(array.flags.writeable).to_be(True)

                array[0] = 500

                reloaded_array = NpyHandler.load(tc.path)
                expect(reloaded_array[0]).to_be(0)

    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            NpyHandler.save(tc.path, np.array([1, 2, 3], dtype=np.int32))
            expect(tc.path).to_be(an_existing_path())
            content = np.load(str(tc.path))
            expect(content).to_be(exactly_equal_to_array(np.array([1, 2, 3], dtype=np.int32)))

    @describe("#matches")
    def _():
        @it("matches only .npy extensions")
        def _(tc: TestContext):
            expect(NpyHandler.matches("test.npy")).to_be(True)
            expect(NpyHandler.matches("test.npy_")).to_be(False)

    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.npy")._handler).to_be(NpyHandler)
