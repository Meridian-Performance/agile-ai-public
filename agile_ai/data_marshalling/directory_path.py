from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from agile_ai.data_marshalling.filesystem import remove_path


class PathLike:
    path: Path

    def __str__(self):
        return str(self.path)

    def exists(self):
        return self.path.exists()

    def remove(self):
        remove_path(self.path)


class DirectoryPath(PathLike):
    path: Path

    def __init__(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        self.path = path

    def sub_directories(self):
        for sub_directory in self.path.iterdir():
            if sub_directory.is_dir():
                yield DirectoryPath(sub_directory)

    def files(self):
        from agile_ai.data_marshalling.file_path import FilePath
        for file in self.path.iterdir():
            if file.is_file():
                yield FilePath(file)

    def ensure_exists(self):
        self.path.mkdir(parents=True, exist_ok=True)

    def __truediv__(self, directory_string):
        return DirectoryPath(self.path / directory_string)

    def __floordiv__(self, directory_string):
        from agile_ai.data_marshalling.file_path import FilePath
        return FilePath(self.path / directory_string)

    def __eq__(self, other):
        if not isinstance(other, DirectoryPath):
            return False
        return self.path == other.path

    @staticmethod
    def home() -> DirectoryPath:
        return DirectoryPath(os.environ["HOME"])
