import os
from pathlib import Path

from agile_ai.data_marshalling.directory_path import DirectoryPath

__test_data_directory = Path(str(os.path.dirname(os.path.abspath(__file__))))
_dataflow_test_directory = DirectoryPath("/tmp/agile-ai-tests")
resources_directory = DirectoryPath(__test_data_directory / "resources")

def reset_and_configure_test():
   __test_data_directory
