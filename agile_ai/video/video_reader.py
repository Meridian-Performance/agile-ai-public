from functools import lru_cache
from pathlib import Path
from typing import Iterable, Union

import cv2

from agile_ai.data_marshalling.file_path import FilePath


class VideoReader:
    video_capture: cv2.VideoCapture

    def __init__(self, path: Union[Path, FilePath, str]):
        self.path = str(path)
        self.next_index = 0
        self.video_capture = cv2.VideoCapture(self.path)

    def reset(self):
        self.next_index = 0
        self.video_capture.release()
        self.video_capture = cv2.VideoCapture(self.path)

    def __next__(self):
        success, image = self.video_capture.read()
        self.next_index += 1
        if not success:
            raise StopIteration
        return image

    def __iter__(self):
        return self

    def read(self) -> Iterable:
        return self

    def get_frame(self, index: int):
        if self.next_index == index:
            return next(self)
        if self.next_index > index:
            self.reset()
        while self.next_index < index:
            next(self)
        return next(self)

    @lru_cache(maxsize=5)
    def __getitem__(self, index: int):
        return self.get_frame(index)