from pathlib import Path
from typing import Iterable, Union

import cv2

from agile_ai.data_marshalling.file_path import FilePath


class VideoReader:
    video_capture: cv2.VideoCapture

    def __init__(self, path: Union[Path, FilePath, str]):
        self.video_capture = cv2.VideoCapture(str(path))

    def __next__(self):
        success, image = self.video_capture.read()
        if not success:
            raise StopIteration
        return image

    def __iter__(self):
        return self

    def read(self) -> Iterable:
        return self
