from pathlib import Path

import pandas as pd

from agile_ai.data_marshalling.file_handler import FileHandler


class ParquetHandler(FileHandler):
    """Class for parquet dataframe handler."""

    @classmethod
    def load(cls, path: Path):
        return pd.read_parquet(str(path))

    @classmethod
    def save(cls, path: Path, object_to_save):
        object_to_save.to_parquet(str(path))

    @classmethod
    def matches(cls, filename: str):
        return filename.endswith(".parquet")
