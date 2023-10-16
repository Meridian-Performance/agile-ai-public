from typing import List, Callable, Dict, Tuple

from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO


class FileInfo(WarehouseObject):
    __metadata__: Marker
    md5_hex: str
    name: str
    extension: str
    tags: List[str]
    file_name: str


class FileInfoIngestor(Processor):
    __services__: Marker
    md5_helper: Md5Helper
    ingestion_configuration: IngestionConfiguration

    class Inputs(IO):
        file_name: str

    class Outputs(IO):
        file_info: ObjectOption[FileInfo]

    def perform(self, inputs: Inputs, outputs: Outputs):
        """
        The full name is the name, followed by key-value pairs
        values may be a dot-seperated list
        """
        file_base_name = inputs.file_name.split("/")[-1]
        extension, key_value_dict = self.parse_key_values(file_base_name)
        if "md5" in key_value_dict:
            md5_hex = "".join(key_value_dict["md5"])
        else:
            file_path = self.ingestion_configuration.source_data_directory // inputs.file_name
            md5_hex = self.md5_helper.digest_file(file_path)
        key_part = KeyLiteral(md5_hex)
        outputs.init_options(key_part)
        file_info = outputs.file_info.object_instance
        file_info.md5_hex = md5_hex
        file_info.file_name = inputs.file_name
        file_info.name = "".join(key_value_dict["name"])
        file_info.extension = extension
        file_info.tags = key_value_dict.get("tags", [])

    def parse_key_values(self, file_name: str) -> Tuple[str, Dict[str, List[str]]]:
        key_value_dict = dict()
        parts = file_name.split(".")
        extension = parts[-1]
        parts = parts[:-1]
        value_parts = []
        key = "name"
        for part in parts:
            if ":" in part:
                if value_parts:
                    key_value_dict[key] = value_parts
                key, _, part = part.partition(":")
                value_parts = []
                if part:
                    value_parts.append(part)
            else:
                value_parts.append(part)
        key_value_dict[key] = value_parts
        return extension, key_value_dict

    resolve: Callable[..., Outputs]
    inputs: Inputs


register_object_class(FileInfo)
