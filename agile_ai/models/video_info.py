from typing import List

from agile_ai.injection import Marker
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class


class VideoInfo(WarehouseObject):
    __metadata__: Marker
    md5_hex: str
    frame_count: int
    width: int
    height: int


register_object_class(VideoInfo)
