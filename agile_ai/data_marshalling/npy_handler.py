from pathlib import Path

import numpy as np

from agile_ai.data_marshalling.file_handler import FileHandler


class NpyHandler(FileHandler):

    @classmethod
    def determine_mmap_mode(self, mmap_mode=None, read_only_memmap=False, read_write_memmap=False,
                            read_copy_memmap=False):
        if read_only_memmap:
            mmap_mode = "r"
        if read_write_memmap:
            mmap_mode = "r+"
        if read_copy_memmap:
            mmap_mode = "c"
        return mmap_mode

    @classmethod
    def load(cls, path: Path, **kwargs):
        mmap_mode = cls.determine_mmap_mode(**kwargs)
        return np.load(str(path), encoding="bytes", mmap_mode=mmap_mode)

    @classmethod
    def save(cls, path: Path, object_to_save, **kwargs):
        np.save(str(path), object_to_save)


    @classmethod
    def matches(cls, filename):
        """Check if filename matches."""
        return filename.endswith(".npy") or filename.endswith(".npz")
