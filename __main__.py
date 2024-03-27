#! /usr/bin/env python

# relative imports
# alternatively, from nearest import ...
import nearest
import gui

from nicegui import ui
from pathlib import Path
import sys
import os

os.chdir(Path(__file__).parent)
print("CWD", os.getcwd())

subdirs = []
for path in Path("data").iterdir():
    if path.is_dir():
        subdirs.append(path)

# gui.draw_selection(subdirs)

img_path = sys.argv[1] if len(sys.argv) > 1 else "data/Italy/IMG20230803112016.jpg"
img_path = Path(img_path)

data_path = sys.argv[2] if len(sys.argv) > 2 else "data/France"
data_path = Path(data_path)

results = nearest.knn_query(img_path, 10, data_path)

for name, similarity in results:
    print(f"{similarity:7.3f} % - {name} {'(identity)' if name == img_path else ''}")

# gui.draw_similar(img_path, results)

# ui.run(title="VWM semestralka", favicon="📷", reload=False)
ui.run(title="VWM semestralka", favicon="📷")