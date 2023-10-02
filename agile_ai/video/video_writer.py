import os
from pathlib import Path

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.video.frame_source import FrameSource


class VideoWriter:
    frame_source: FrameSource
    output_path: Path

    def __init__(self, output_path: [Path, FilePath], frame_source: FrameSource):
        self.output_path = output_path
        self.frame_source = frame_source

    def write(self):
        input_path = self.frame_source.get_input_path()
        output_path = self.output_path
        command = f"ffmpeg -r 30 -f image2 -i {input_path} -vcodec libx264 -crf 25 -pix_fmt yuv420p {output_path}"
        os.system(command)
