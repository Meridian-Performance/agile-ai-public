from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection import Marker
from agile_ai.memoization.warehouse_object import WarehouseObject


class FileSeries(WarehouseObject):
    __metadata__: Marker
    extension_by_key: str
    count: str

    __objects__: Marker

    def __getitem__(self, item: int):
        pass

    def __setitem__(self, index: int, value: np.ndarray):
        pass

    def fetch(self, directory_path: DirectoryPath):
        pass

    def store(self, directory_path: DirectoryPath):
        pass
