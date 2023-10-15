from typing import List, Callable, Dict, Tuple

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.memoization.warehouse_object import WarehouseObject
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

    class Inputs(IO):
        file_path: FilePath

    class Outputs(IO):
        file_info: ObjectOption[FileInfo]

    def perform(self, inputs: Inputs, outputs: Outputs):
        """
        The full name is the name, followed by key-value pairs
        values may be a dot-seperated list
        """
        file_name = inputs.file_path.path.parts[-1]
        extension, key_value_dict = self.parse_key_values(file_name)
        if "md5" in key_value_dict:
            md5_hex = "".join(key_value_dict["md5"])
        else:
            md5_hex = self.md5_helper.digest_file(inputs.file_path)
        file_info = FileInfo()
        file_info.md5_hex = md5_hex
        file_info.file_name = file_name
        file_info.name = "".join(key_value_dict["name"])
        file_info.extension = extension
        file_info.tags = key_value_dict.get("tags", [])
        key_part = KeyLiteral(md5_hex)
        outputs.init_options(key_part)
        outputs.file_info.set(file_info)

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
