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

    def populate_frames(self):
        for i, frame in enumerate(self.frames):
            print("Saving frame", i)
            (self.frame_directory // f"frame_{i:008d}.png").put(frame)

    def get_input_path(self):
        self.populate_frames()
        input_path = self.frame_directory // "frame_%08d.png"
        return input_path
