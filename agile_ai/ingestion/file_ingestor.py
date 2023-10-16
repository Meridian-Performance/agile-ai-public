from typing import List, Callable, Dict, Tuple
from agile_ai.ingestion.file_info_ingestor import FileInfo
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection import Marker
from agile_ai.memoization.warehouse_object import WarehouseObject


class File(WarehouseObject):
    __metadata__: Marker

    def fetch(self, directory_path: DirectoryPath):
        pass

    def store(self, directory_path: DirectoryPath):
        pass


class FileIngestor(Processor):
    __services__: Marker

    class Inputs(IO):
        file_info: ObjectOption[FileInfo]

    class Outputs(IO):
        file: ObjectOption[File]

    def perform(self, inputs: Inputs, outputs: Outputs):
        pass

    resolve: Callable[..., Outputs]
    inputs: Inputs
