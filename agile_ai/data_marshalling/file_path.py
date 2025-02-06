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
        try:
            return self._handler.load(self.path)
        except Exception as e:
            print("Error loading", self.path)
            print(e)
            raise e

    def put(self, object):
        DirectoryPath(self.path.parent).ensure_exists()
        return self._handler.save(self.path, object)

    def __eq__(self, other):
        if not isinstance(other, FilePath):
            return False
        return self.path == other.path

def add_handlers():
    from agile_ai.data_marshalling.txt_handler import TxtHandler
    FilePath.add_handler(TxtHandler)
    try:
        from agile_ai.data_marshalling.obj_handler import ObjHandler
        FilePath.add_handler(ObjHandler)
    except ModuleNotFoundError as e:
        print("Unable to import ObjHandler:", e)
    from agile_ai.data_marshalling.pkl_handler import PklHandler
    FilePath.add_handler(PklHandler)
    try:
        from agile_ai.data_marshalling.yaml_handler import YamlHandler
        FilePath.add_handler(YamlHandler)
    except ModuleNotFoundError:
        print("Unable to import YamlHandler, pyyaml module not found")
    from agile_ai.data_marshalling.json_handler import JsonHandler
    FilePath.add_handler(JsonHandler)
    from agile_ai.data_marshalling.npy_handler import NpyHandler
    FilePath.add_handler(NpyHandler)
    from agile_ai.data_marshalling.npz_handler import NpzHandler
    FilePath.add_handler(NpzHandler)
    from agile_ai.data_marshalling.csv_handler import CsvHandler
    FilePath.add_handler(CsvHandler)
    from agile_ai.data_marshalling.image_handler import ImageHandler
    FilePath.add_handler(ImageHandler)
    from agile_ai.data_marshalling.parquet_handler import ParquetHandler
    FilePath.add_handler(ParquetHandler)


add_handlers()