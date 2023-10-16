from typing import Tuple

import numpy as np
import pylab

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection.decorators import Marker
from agile_ai.video.frame_source import FrameSource
from agile_ai.video.video_reader import VideoReader
from agile_ai.video.video_writer import VideoWriter
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, TCBase, describe, it
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    frame_source: FrameSource
    video_writer: VideoWriter
    output_path: FilePath

def get_color_square(color: Tuple[int, int, int]):
    square = np.empty((128, 256, 3), dtype=np.uint8)
    square[:, :] = color
    return square


@pyne
def video_writer_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        frame_directory = tc.test_directory / "test_frames"
        tc.output_path = tc.test_directory / "output.mp4"
        jet = pylab.cm.jet
        colors = (np.array(jet(np.linspace(0, 1, 25)))[:, :3] * 255).astype(np.uint8)
        frame_list = [get_color_square(c) for c in colors]
        tc.frame_source = FrameSource(frame_directory).with_frames(frame_list)
        tc.video_writer = VideoWriter(tc.output_path, tc.frame_source)

    @describe("#write")
    def _():
        @it("creates an mp4 file with 25 frames")
        def _(tc: TestContext):
            tc.video_writer.write()
            expect(tc.output_path).to_be(an_existing_path())
            video_reader = VideoReader(tc.output_path)
            frames = list(video_reader.read())
            expect(frames).to_have_length(25)
            first_frame = frames[0]
            expect(first_frame.shape).to_be((128, 256, 3))
            expect(tuple(first_frame[0, 0])).to_be((125, 0, 0))

