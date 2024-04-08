from pathlib import Path


from agile_ai.data_marshalling.file_handler import FileHandler


class NpzHandler(FileHandler):

    @classmethod
    def load(cls, path: Path, **kwargs):
        import numpy as np
        npz_file = np.load(str(path), encoding="bytes")
        array = npz_file.get(npz_file.files[0])
        return array

    @classmethod
    def save(cls, path: Path, object_to_save, **kwargs):
        import numpy as np
        np.savez_compressed(str(path), object_to_save)


    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".npz")
