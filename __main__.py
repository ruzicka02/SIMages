#! /usr/bin/env python

# relative imports
# alternatively, from nearest import ...
import nearest
import gui

from nicegui import ui
from pathlib import Path
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else "data/Italy/IMG20230803112016.jpg"
img_path = Path(img_path)

data_path = sys.argv[2] if len(sys.argv) > 2 else "data/France"
data_path = Path(data_path)

results = nearest.knn_query(img_path, 10, data_path)

for name, similarity in results:
    print(f"{similarity:7.3f} % - {name} {'(identity)' if name == img_path else ''}")

gui.draw_gui(img_path, results)

ui.run()