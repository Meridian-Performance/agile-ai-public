from pathlib import Path

from agile_ai.data_marshalling.file_handler import FileHandler


class CsvHandler(FileHandler):
    @classmethod
    def load(cls, path: Path):
        import csv
        with path.open("r") as file:
            reader = csv.reader(file)
            return list(reader)

    @classmethod
    def save(cls, path: Path, object_to_save):
        import csv
        with path.open("w") as file:
            writer = csv.writer(file)
            writer.writerows(object_to_save)

    @classmethod
    def matches(cls, filename):
        return filename.endswith(".csv")
