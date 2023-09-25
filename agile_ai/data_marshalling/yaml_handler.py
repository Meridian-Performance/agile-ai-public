"""Handler implemention for yaml."""
from pathlib import Path

from yaml import load, dump, Loader

from agile_ai.data_marshalling.file_handler import FileHandler


class YamlHandler(FileHandler):
    @classmethod
    def load(cls, path: Path, **kwargs):
        with path.open("r") as file:
            return load(file, Loader=Loader)

    @classmethod
    def save(cls, path: Path, object_to_save):
        with path.open("w") as file:
            dump(object_to_save, file)

    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".yaml")
