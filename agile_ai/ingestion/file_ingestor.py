from typing import Callable

from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling import filesystem
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.ingestion.file_info_ingestor import FileInfo, FileInfoIngestor
from agile_ai.injection import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO


class File(WarehouseObject):
    __metadata__: Marker

    __objects__: Marker
    file_info: ObjectOption[FileInfo]

    @property
    def path(self) -> FilePath:
        extension = self.file_info.get().extension
        return self.get_object_path() // f"file.{extension}"


class FileIngestor(Processor):
    __services__: Marker
    ingestion_configuration: IngestionConfiguration

    class Inputs(IO):
        file_info: ObjectOption[FileInfo]

    class Outputs(IO):
        file: ObjectOption[File]

    def perform(self, inputs: Inputs, outputs: Outputs):
        file = outputs.file()
        file.file_info = inputs.file_info
        file.get_object_path().ensure_exists()
        file_path = (self.ingestion_configuration.source_data_directory // file.file_info.get().file_name)
        filesystem.copy(file_path, file.path)

    resolve: Callable[..., Outputs]
    inputs: Inputs


register_object_class(File)
