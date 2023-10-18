from typing import List

from agile_ai.injection import Marker
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class


class FileInfo(WarehouseObject):
    __metadata__: Marker
    md5_hex: str
    name: str
    extension: str
    tags: List[str]
    file_name: str

register_object_class(FileInfo)
