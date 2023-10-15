import subprocess

from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection.interfaces import Service


class Md5Helper(Service):
    def digest_file(self, file_path: FilePath) -> str:
        completed_process = subprocess.run(f"md5sum {file_path}", capture_output=True, shell=True)
        return completed_process.stdout.decode("U8").split()[0]
