from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.models.file import File


class PandasDataframe(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extension = "parquet"


register_object_class(PandasDataframe)
