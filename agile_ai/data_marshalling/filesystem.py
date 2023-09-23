from pathlib import Path


def remove_path(path):
    import shutil
    path = Path(str(path))
    if path.exists():
        shutil.rmtree(path)
