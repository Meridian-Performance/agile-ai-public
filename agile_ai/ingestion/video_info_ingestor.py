from typing import Callable

from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.injection import Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.models.file import File
from agile_ai.models.video_info import VideoInfo
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai.video.video_reader import VideoReader


class VideoInfoIngestor(Processor):
    __services__: Marker
    md5_helper: Md5Helper
    ingestion_configuration: IngestionConfiguration

    class Inputs(IO):
        file: ObjectOption[File]

    class Outputs(IO):
        video_info: ObjectOption[VideoInfo]

    resolve: Callable[..., Outputs]
    inputs: Inputs

    def perform(self, inputs: Inputs, outputs: Outputs):
        """
        The full name is the name, followed by key-value pairs
        values may be a dot-seperated list
        """
        file = inputs.file.get()
        md5_hex = file.file_info.get().md5_hex
        file_reader = VideoReader(file.path)
        frame_count = 0
        width = 0
        height = 0
        for frame in file_reader:
            frame_count += 1
            width = frame.shape[1]
            height = frame.shape[0]

        video_info = outputs.video_info()
        video_info.md5_hex = md5_hex
        video_info.frame_count = frame_count
        video_info.width = width
        video_info.height = height

