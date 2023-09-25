from pathlib import Path

from agile_ai.data_marshalling.file_handler import FileHandler
from agile_ai.geometry.wavefront_obj import WavefrontObj


class ObjHandler(FileHandler):
    @classmethod
    def load(cls, path: Path):
        with path.open("r") as file:
            lines = file.readlines()
            mesh = WavefrontObj.mesh_from_lines(lines)
        return mesh

    @classmethod
    def save(cls, path: Path, object_to_save):
        lines = WavefrontObj.mesh_to_lines(object_to_save)
        with path.open("w") as file:
            for line in lines:
                print(line, file=file)

    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".obj")
