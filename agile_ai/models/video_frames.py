import numpy as np

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class


class VideoFrames(WarehouseObject):
    __metadata__: Marker
    extension: str
    count: str

    __objects__: Marker

    def series_file_path(self, series_name: str, series_index: int) -> FilePath:
        return self.get_series_directory(series_name) // f'{series_index:08d}.{self.extension}'

    def get_series_directory(self, series_name: str):
        return self.get_object_path() / series_name

    def get_frames_directory(self):
        return self.get_series_directory("frames")

    def __len__(self):
        return self.count

    def __getitem__(self, index: int) -> np.ndarray:
        if index >= self.count:
            raise IndexError
        return self.series_file_path("frames", index).get()

    def __setitem__(self, index: int, value: np.ndarray):
        frame_file_path = self.series_file_path("frames", index)
        frame_file_path.put(value)
        return value

register_object_class(VideoFrames)
