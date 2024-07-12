from typing import List, Callable, Dict, Tuple, Optional, Union

from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyLiteral, ExcludedKey
from agile_ai.models.file_info import FileInfo
from agile_ai.processing.processor import Processor
from agile_ai.processing.processor_io import IO
from agile_ai.processing.typed_scope import TypedScope


class FileInfoIngestor(Processor):
    __services__: Marker
    md5_helper: Md5Helper
    ingestion_configuration: IngestionConfiguration

    class Inputs(IO):
        base_directory: Union[str, DirectoryPath, ExcludedKey] = None
        file_name: str
        key_value_string: str = ""

    class Outputs(IO):
        file_info: ObjectOption[FileInfo]

    resolve: Callable[..., Outputs]
    inputs: Inputs

    def perform(self, inputs: Inputs, outputs: Outputs):
        """
        The full name is the name, followed by key-value pairs
        values may be a dot-seperated list
        """
        file_base_name = inputs.file_name.split("/")[-1]
        base_directory = inputs.base_directory if inputs.base_directory else self.ingestion_configuration.source_data_directory
        file_path = DirectoryPath(base_directory) // inputs.file_name
        extension, key_value_dict = self.parse_key_values(file_base_name, inputs.key_value_string)
        if "md5" in key_value_dict:
            md5_hex = "".join(key_value_dict["md5"])
        else:
            md5_hex = self.md5_helper.digest_file(file_path)
        key_part = KeyLiteral(md5_hex)
        file_info = FileInfo().with_key_part(key_part)
        file_info.md5_hex = md5_hex
        file_info.file_name = inputs.file_name
        file_info.name = "".join(key_value_dict["name"])
        file_info.extension = extension
        file_info.tags = key_value_dict.get("tags", [])
        outputs.file_info(file_info)

    def parse_key_values(self, file_name: str, key_values_string: str) -> Tuple[str, Dict[str, List[str]]]:
        key_value_dict = dict(name="")
        parts = file_name.split(".")
        extension = parts.pop(-1).lower()
        value_parts = []
        key_value_dict["name"] = parts.pop(0)
        if key_values_string:
            parts = key_values_string.split(".")
        key = None
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
