import os
from pathlib import Path

def list_subdirs():
    os.chdir(Path(__file__).parent)
    print("CWD", os.getcwd())

    subdirs = []
    for path in Path("data").iterdir():
        if path.is_dir():
            subdirs.append(path)

    return subdirs