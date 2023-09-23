# Import all data types
from pathlib import Path
from typing import Union


class FileHandler:
    """Generic class for Handler objects."""
    @classmethod
    def load(cls, path: Path):
        pass

    @classmethod
    def save(cls, path: Path, object_to_save):
        pass

    @classmethod
    def matches(cls, filename):
        """Check if class matches path extension."""
        raise NotImplementedError



