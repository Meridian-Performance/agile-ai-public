from typing import Callable

import pandas as pd

from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.models.file import File


class PandasDataframe(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extension = "parquet"

    load_file: Callable[..., pd.DataFrame]


register_object_class(PandasDataframe)
