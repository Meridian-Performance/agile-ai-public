from pathlib import Path

import numpy as np

from agile_ai.data_marshalling.npz_handler import NpzHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import exactly_equal_to_array, an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit
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
        tc.path = tc.test_directory // "test.npz"

    @describe("#load")
    def _():
        @before_each
        def _(tc: TestContext):
            np.savez_compressed(str(tc.path), tc.array)

        @it("loads the numpy array")
        def _(tc: TestContext):
            array = NpzHandler.load(tc.path)
            expect(array).to_be_a(np.ndarray)
            expect(array).to_have_length(100)
            expect(array).to_be(exactly_equal_to_array(tc.array))
            expect(array.flags.owndata).to_be(True)
    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            NpzHandler.save(tc.path, np.array([1, 2, 3], dtype=np.int32))
            expect(tc.path).to_be(an_existing_path())
            npz_file = np.load(str(tc.path), encoding="bytes")
            content = npz_file.get(npz_file.files[0])
            expect(content).to_be(exactly_equal_to_array(np.array([1, 2, 3], dtype=np.int32)))

    @describe("#matches")
    def _():
        @it("matches only .npz extensions")
        def _(tc: TestContext):
            expect(NpzHandler.matches("test.npz")).to_be(True)
            expect(NpzHandler.matches("test.npz_")).to_be(False)

    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.npz")._handler).to_be(NpzHandler)
