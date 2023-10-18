import numpy as np

from agile_ai.configuration import configure_warehouse
from agile_ai.ingestion.video_frame_extractor import VideoFrameExtractor
from agile_ai.injection.decorators import Marker
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.models.file import File
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
    video_file: File

@pyne
def video_frame_extractor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        configure_warehouse()
        tc.video_file = (File()
                         .with_key_part(KeyLiteral("some_file_key"))
                         .allocate_storage()
                         .init_options(KeyLiteral("some_key"))
                         .with_extension("mp4")
                         .store_options()
                         .copy_from_file_path((resources_directory / "mp4" // "jet_colors_25.mp4"))
                         .put()
                         )


    @describe("#perform")
    def _():
        @it("returns a VideoFrames object populated with video frames and the count")
        def _(tc: TestContext):
            extractor = VideoFrameExtractor()
            extractor.inputs.video_file(tc.video_file)
            extractor.inputs.extension = "npz"
            video_frames = extractor.resolve().video_frames.get()
            expect(video_frames.count).to_be(25)
            expect(video_frames.extension).to_be("npz")
            expect(video_frames[0]).to_be_a(np.ndarray)
            expect(video_frames[24]).to_be_a(np.ndarray)

