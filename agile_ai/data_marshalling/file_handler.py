# Import all data types
from pathlib import Path


class FileHandler:
    """Generic class for Handler objects."""
    @classmethod
    def load(cls, path: Path):
        raise NotImplementedError

    @classmethod
    def save(cls, path: Path, object_to_save):
        raise NotImplementedError

    @classmethod
    def matches(cls, filename):
        """Check if class matches path extension."""
        raise NotImplementedError



