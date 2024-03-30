import os
from pathlib import Path

def chdir():
    os.chdir(Path(__file__).parent)
    print("CWD", os.getcwd())

def list_subdirs():
    chdir()

    subdirs = []
    for path in Path("data").iterdir():
        if path.is_dir():
            subdirs.append(path)

    return subdirs