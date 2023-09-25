from pathlib import Path
from agile_ai.data_marshalling.file_handler import FileHandler


class ImageHandler(FileHandler):
    @classmethod
    def load(cls, path: Path):
        ext = path.suffix
        from imageio.v2 import imread
        return imread(path, format=ext)

    @classmethod
    def save(cls, path: Path, object_to_save):
        ext = path.suffix
        from imageio import imsave
        imsave(path, object_to_save, format=ext)

    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".gif")
