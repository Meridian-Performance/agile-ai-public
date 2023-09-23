from pathlib import Path

from agile_ai.data_marshalling.file_handler import FileHandler


class TxtHandler(FileHandler):
    @classmethod
    def load(cls, path: Path):
        with path.open("r") as fh:
            return fh.read()
    @classmethod
    def save(cls, path: Path, object_to_save):
        with path.open("w") as fh:
            fh.write(object_to_save)
    @classmethod
    def matches(cls, filename):
        return filename.endswith(".txt")
