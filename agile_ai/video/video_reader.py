from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Union

import cv2
import numpy as np

from agile_ai.data_marshalling.file_path import FilePath


class ColorType(Enum):
    RGB = "RGB"
    BGR = "BGR"
    GRAY = "GRAY"
    LAB = "LAB"

    @staticmethod
    def get_convert_type(source: "ColorType", destination: "ColorType"):
        return getattr(cv2, f'COLOR_{source.value}2{destination.value}')

    @staticmethod
    def convert(image, source: "ColorType", destination: "ColorType"):
        if source == destination:
            return image
        cv2_convert_type = ColorType.get_convert_type(source, destination)
        return cv2.cvtColor(image, cv2_convert_type)


class VideoReader:
    video_capture: cv2.VideoCapture
    source_color: ColorType
    output_color: ColorType

    def __init__(self, path: Union[Path, FilePath, str], source_color=ColorType.BGR, output_color=ColorType.RGB):
        self.path = str(path)
        self.next_index = 0
        self.video_capture = cv2.VideoCapture(self.path)
        self.source_color = source_color
        self.output_color = output_color

    def reset(self):
        self.next_index = 0
        self.video_capture.release()
        self.video_capture = cv2.VideoCapture(self.path)

    def compute_count(self) -> int:
        self.reset()
        try:
            self.seek(np.inf)
        except StopIteration:
            pass
        count = self.next_index - 1
        self.reset()
        return count

    def read_next(self, discard=False):
        success, image = self.video_capture.read()
        self.next_index += 1
        if not success:
            raise StopIteration
        if discard:
            return None
        return ColorType.convert(image, self.source_color, self.output_color)

    def __next__(self):
        return self.read_next()

    def __iter__(self):
        return self

    def stream(self) -> Iterable:
        return self

    def read(self) -> Iterable:
        return self

    def seek(self, index: int):
        if self.next_index == index:
            return
        if self.next_index > index:
            self.reset()
        while self.next_index < index:
            self.read_next(discard=True)

    def get_frame(self, index: int):
        self.seek(index)
        return next(self)

    @lru_cache(maxsize=5)
    def __getitem__(self, index: int):
        return self.get_frame(index)

    def get_element(self, index: int):
        return self.get_frame(index)