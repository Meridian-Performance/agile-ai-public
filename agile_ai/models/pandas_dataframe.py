from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.models.file import File


class PandasDataframe(File):
    def __init__(self):
        self.extension = "parquet"
        super().__init__()


register_object_class(PandasDataframe)
