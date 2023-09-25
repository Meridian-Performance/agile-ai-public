"""Handler implemention for numpy."""
from pathlib import Path

from agile_ai.data_marshalling.file_handler import FileHandler

try:
    import cPickle as pickle
except ImportError:
    import pickle


class PklHandler(FileHandler):
    """Class for numpy Handler."""

    @classmethod
    def load(cls, path: Path):
        with path.open("rb") as file:
            return pickle.load(file)

    @classmethod
    def save(cls, path: Path, object_to_save):
        with path.open("wb") as file:
            pickle.dump(object_to_save, file)

    @classmethod
    def matches(cls, filename: str):
        return filename.endswith(".pkl")
