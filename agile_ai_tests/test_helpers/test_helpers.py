import os
from pathlib import Path

from agile_ai.data_marshalling.directory_path import DirectoryPath
from agile_ai.data_marshalling.filesystem import remove_path
from agile_ai.injection.decorators import reset_autowire
from agile_ai_tests.test_helpers.pyne_test_helpers import TCBase

__test_data_directory = Path(str(os.path.dirname(os.path.abspath(__file__))))
_agile_ai_test_directory = DirectoryPath("/tmp/agile-ai-tests")
resources_directory = DirectoryPath(__test_data_directory / "resources")

def reset_and_configure_test():
   _agile_ai_test_directory.remove()
   _agile_ai_test_directory.ensure_exists()
   reset_autowire()

TCBase.set_test_directory(_agile_ai_test_directory)