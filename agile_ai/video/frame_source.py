from typing import Iterable

from agile_ai.data_marshalling.directory_path import DirectoryPath


class FrameSource:
    frame_directory: DirectoryPath
    frames: Iterable

    def __init__(self, frame_directory: DirectoryPath):
        self.frame_directory = frame_directory

    def with_frames(self, frames: Iterable):
        self.frames = frames
        return self

    def populate_frames(self, ext="png"):
        for i, frame in enumerate(self.frames):
            print("Saving frame", i)
            (self.frame_directory // f"frame_{i:008d}.{ext}").put(frame)

    def get_input_path(self):
        input_path = self.frame_directory // "frame_%08d.png"
        return input_path
