import json
from pathlib import Path

from agile_ai.data_marshalling.file_handler import FileHandler


class JsonHandler(FileHandler):

    @classmethod
    def load(cls, path: Path, **kwargs):
        with path.open("r") as file:
            return json.load(file, **kwargs)

    @classmethod
    def save(cls, path: Path, object_to_save, **kwargs):
        with path.open("w") as file:
            json.dump(object_to_save, file, **kwargs)

    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".json")
