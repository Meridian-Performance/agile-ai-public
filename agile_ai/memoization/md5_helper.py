import subprocess

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection.interfaces import Service


class Md5Helper(Service):
    def digest_file(self, file_path: FilePath) -> str:
        command_string = f"md5sum '{file_path}'"
        completed_process = subprocess.run(command_string, capture_output=True, shell=True)
        output_string = completed_process.stdout.decode("U8")
        return output_string.split()[0]
