from typing import Callable, Union

from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import ExcludedKey
from agile_ai.models.file import File
from agile_ai.models.file_info import FileInfo
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO


class FileIngestor(Processor):
    __services__: Marker
    ingestion_configuration: IngestionConfiguration

    class Inputs(IO):
        file_info: ObjectOption[FileInfo]
        base_directory: Union[str, DirectoryPath, ExcludedKey] = None

    class Outputs(IO):
        file: ObjectOption[File]

    resolve: Callable[..., Outputs]
    inputs: Inputs

    def perform(self, inputs: Inputs, outputs: Outputs):
        file = outputs.file()
        file.file_info = inputs.file_info
        file.get_object_path().ensure_exists()
        base_directory = inputs.base_directory if inputs.base_directory else self.ingestion_configuration.source_data_directory
        file_path = (DirectoryPath(base_directory) // file.file_info.get().file_name)
        file.copy_from_file_path(file_path)



