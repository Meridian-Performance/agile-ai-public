from typing import Optional

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.memoization.warehouse_service import register_object_class, set_partition_name, set_warehouse_directory


def configure_warehouse(warehouse_directory: Optional[DirectoryPath] = None, partition_name: Optional[str] = None):
    if warehouse_directory:
        set_warehouse_directory(warehouse_directory)
    if partition_name:
        set_partition_name(partition_name)
    from agile_ai.ingestion.file_info_ingestor import FileInfo
    from agile_ai.ingestion.file_ingestor import File
    register_object_class(FileInfo)
    register_object_class(File)
