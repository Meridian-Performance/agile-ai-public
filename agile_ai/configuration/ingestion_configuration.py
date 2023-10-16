from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.injection.interfaces import Service


class IngestionConfiguration(Service):
    source_data_directory: DirectoryPath
