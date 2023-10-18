from typing import List, Callable, Dict, Tuple

from agile_ai.models.file import File
from agile_ai.injection import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.models.file_info import FileInfo
from agile_ai.models.video_frames import VideoFrames
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai.video.video_reader import VideoReader


class VideoFrameExtractor(Processor):
    __services__: Marker
    class Inputs(IO):
        video_file: ObjectOption[File]

    class Outputs(IO):
        video_frames: ObjectOption[VideoFrames]

    resolve: Callable[..., Outputs]
    inputs: Inputs

    def perform(self, inputs: Inputs, outputs: Outputs):
        video_reader = VideoReader(inputs.video_file.get().path)
        video_frames = outputs.video_frames()
        video_frames.extension = "npz"
        index = 0
        for index, frame in enumerate(video_reader):
            video_frames[index] = frame
        video_frames.count = index + 1

