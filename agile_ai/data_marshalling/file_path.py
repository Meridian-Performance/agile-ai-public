from pathlib import Path
from typing import Set, Type

from agile_ai.data_marshalling.directory_path import PathLike, DirectoryPath
from agile_ai.data_marshalling.file_handler import FileHandler


class FilePath(PathLike):
    handlers: Set[Type[FileHandler]] = set()

    @classmethod
    def add_handler(cls, handler: Type[FileHandler]):
        cls.handlers.add(handler)

    def __init__(self, path):
        self._handler = None
        if isinstance(path, str):
            path = Path(path)
        path_str = str(path)
        for handler in self.handlers:
            if handler.matches(path_str):
                self._handler = handler
                break
        self.path = path

    def touch(self):
        DirectoryPath(self.path.parent).ensure_exists()
        with self.path.open("w"):
            pass

    def get(self):
        return self._handler.load(self.path)

    def put(self, object):
        DirectoryPath(self.path.parent).ensure_exists()
        return self._handler.save(self.path, object)

    def __eq__(self, other):
        if not isinstance(other, FilePath):
            return False
        return self.path == other.path

def add_handlers():
    from agile_ai.data_marshalling.txt_handler import TxtHandler
    from agile_ai.data_marshalling.obj_handler import ObjHandler
    from agile_ai.data_marshalling.pkl_handler import PklHandler
    from agile_ai.data_marshalling.yaml_handler import YamlHandler
    from agile_ai.data_marshalling.json_handler import JsonHandler
    from agile_ai.data_marshalling.npy_handler import NpyHandler
    from agile_ai.data_marshalling.npz_handler import NpzHandler
    from agile_ai.data_marshalling.csv_handler import CsvHandler
    from agile_ai.data_marshalling.image_handler import ImageHandler
    from agile_ai.data_marshalling.parquet_handler import ParquetHandler
    FilePath.add_handler(TxtHandler)
    FilePath.add_handler(ObjHandler)
    FilePath.add_handler(PklHandler)
    FilePath.add_handler(YamlHandler)
    FilePath.add_handler(JsonHandler)
    FilePath.add_handler(NpyHandler)
    FilePath.add_handler(NpzHandler)
    FilePath.add_handler(CsvHandler)
    FilePath.add_handler(ImageHandler)
    FilePath.add_handler(ParquetHandler)


add_handlers()