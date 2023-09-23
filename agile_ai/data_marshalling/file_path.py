from pathlib import Path
from typing import Set, Type

from agile_ai.data_marshalling.directory_path import PathLike
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
        with self.path.open("w"):
            pass

    def get(self):
        return self._handler.load(self.path)

    def put(self, object):
        return self._handler.save(self.path, object)

def add_handlers():
    from agile_ai.data_marshalling.txt_handler import TxtHandler
    FilePath.add_handler(TxtHandler)


add_handlers()
