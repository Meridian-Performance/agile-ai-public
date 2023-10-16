from pathlib import Path


def remove_path(path):
    import shutil
    path = Path(str(path))
    if path.exists():
        shutil.rmtree(path)


def copy(src, dest):
    import shutil
    shutil.copy(str(src), str(dest))