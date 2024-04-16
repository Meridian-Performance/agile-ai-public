from typing import Iterable

from agile_ai.data_marshalling.directory_path import DirectoryPath


class FrameSource:
    frame_directory: DirectoryPath
    frames: Iterable
    ext: str

    def __init__(self, frame_directory: DirectoryPath, ext="png"):
        self.frame_directory = frame_directory
        self.ext = ext

    def with_frames(self, frames: Iterable):
        self.frames = frames
        return self

    def populate_frames(self):
        for i, frame in enumerate(self.frames):
            print("Saving frame", i)
            (self.frame_directory // f"frame_{i:008d}.{self.ext}").put(frame)
        return self

    def get_input_path(self):
        input_path = self.frame_directory // f"frame_%08d.{self.ext}"
        return input_path
