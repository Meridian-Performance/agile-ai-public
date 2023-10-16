from pathlib import Path

import numpy as np
from imageio import imsave
from imageio.v2 import imread

from agile_ai.data_marshalling.image_handler import ImageHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path, exactly_equal_to_array
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
    path: Path
    image: np.ndarray

@pyne
def png_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.image = np.zeros((32, 32, 3), dtype=np.uint8)
        tc.image[5, 5, :] = (10, 20, 30)
        tc.image[10, 10, :] = (25, 35, 45)
        tc.image[20, 5, :] = (255, 255, 0)

    @describe("when the file type is png")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.path = tc.test_directory.path / "file.png"

        @describe("#load")
        def _():
            @it("returns the file contents")
            def _(tc: TestContext):
                imsave(str(tc.path), tc.image)
                content = ImageHandler.load(tc.path)
                expect(content).to_be(exactly_equal_to_array(tc.image))

        @describe("#save")
        def _():
            @it("saves the content to a file")
            def _(tc: TestContext):
                ImageHandler.save(tc.path, tc.image)
                content = imread(tc.path)
                expect(tc.path).to_be(an_existing_path())
                expect(content).to_be(exactly_equal_to_array(tc.image))

    @describe("when the file type is jpg")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.path = tc.test_directory.path / "file.jpg"

        @describe("#load")
        def _():
            @it("returns the file contents")
            def _(tc: TestContext):
                tc.image[:] = 255
                imsave(str(tc.path), tc.image)
                content = ImageHandler.load(tc.path)
                expect(content).to_be(exactly_equal_to_array(tc.image))

        @describe("#save")
        def _():
            @it("saves the content to a file")
            def _(tc: TestContext):
                tc.image[:] = 255
                ImageHandler.save(tc.path, tc.image)
                content = imread(tc.path)
                expect(tc.path).to_be(an_existing_path())
                expect(content).to_be(exactly_equal_to_array(tc.image))

    @describe("#matches")
    def _():
        @it("matches .png extension")
        def _(tc: TestContext):
            expect(ImageHandler.matches("test.png")).to_be(True)

        @it("matches .jpg extension")
        def _(tc: TestContext):
            expect(ImageHandler.matches("test.jpg")).to_be(True)

        @it("matches .gif extension")
        def _(tc: TestContext):
            expect(ImageHandler.matches("test.gif")).to_be(True)

    @describe("when the file type is gif")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.path = tc.test_directory.path / "file.gif"

        @describe("#load")
        def _():
            @it("returns the file contents")
            def _(tc: TestContext):
                imsave(str(tc.path), tc.image)
                content = ImageHandler.load(tc.path)
                expect(content).to_be(exactly_equal_to_array(tc.image))

        @describe("#save")
        def _():
            @it("saves the content to a file")
            def _(tc: TestContext):
                ImageHandler.save(tc.path, tc.image)
                content = imread(tc.path)
                expect(tc.path).to_be(an_existing_path())
                expect(content).to_be(exactly_equal_to_array(tc.image))

    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.png")._handler).to_be(ImageHandler)
