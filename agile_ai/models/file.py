from agile_ai.data_marshalling import filesystem
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_object import WarehouseObject
from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.models.file_info import FileInfo


class File(WarehouseObject):
    __metadata__: Marker
    extension: str

    __objects__: Marker
    file_info: ObjectOption[FileInfo]

    def get_extension(self):
        if hasattr(self, "extension") and self.extension:
            return self.extension
        else:
            return self.file_info.get().extension

    @property
    def path(self) -> FilePath:
        extension = self.get_extension()
        return self.get_object_path() // f"file.{extension}"

    def copy_from_file_path(self, source_file_path: FilePath):
        filesystem.copy(source_file_path, self.path)
        return self

    def with_extension(self, extension: str):
        self.extension = extension
        self.file_info().extension = extension
        return self


register_object_class(File)
