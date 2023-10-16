from agile_ai.injection.decorators import Marker
from agile_ai.video.video_reader import VideoReader
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    video_reader: VideoReader

@pyne
def video_reader_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.video_reader = VideoReader(resources_directory / "mp4" // "jet_colors_25.mp4")
    @describe("#read")
    def _():
        @it("reads all frames")
        def _(tc: TestContext):
            frames = list(tc.video_reader.read())
            expect(frames).to_have_length(25)
            first_frame = frames[0]
            expect(first_frame.shape).to_be((128, 256, 3))
            expect(tuple(first_frame[0, 0])).to_be((125, 0, 0))

