"""
Using precomputed weights, find the closest photos to a photo.
"""

import numpy as np
from pathlib import Path
import sys

def knn_query(img: Path, k: int, query_data: Path | None = None) -> list[tuple[Path, float]]:
    """
    Select k items from query_data directory most similar to img. When query_data is not given,
    assume the parent directory of img (self-join).
    """
    if not query_data:
        query_data = img.parent

    # target features of img
    with open(img.parent / "img_order.txt", "r") as f:
        names = f.read().split()

    img_index = names.index(img.name)

    img_features = np.load(img.parent / "features.npz")['arr_0'][img_index,:]  # selection from "archive" needed for npz

    # features of matched elements
    with open(query_data / "img_order.txt", "r") as f:
        names = f.read().split()

    feats = np.load(query_data / "features.npz")['arr_0']  # selection from "archive" needed for npz
    imgs = feats.shape[0]

    print(f"{imgs} images loaded")

    assert imgs == len(names), "Mismatch detected between the image names and feature matrix."

    # cosine (dot-product) similarity... higher is better
    # relative to the maximum value (exact match)
    img_norm = np.linalg.norm(img_features)
    sims = [np.dot(img_features, feats[i]) / img_norm / np.linalg.norm(feats[i]) for i in range(imgs)]

    result = []
    for s in sorted(sims)[:-k-1:-1]:  # top k, reversed (higher is better)
        name = names[np.where(sims == s)[0][0]]
        result.append((Path(query_data / name), 100 * s))

    return result

    # time benchmark - entire similarity matrix
    # np.array([[np.dot(feats[i], feats[j]) for i in range(imgs)] for j in range(imgs)])

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "data/Italy/IMG20230803112016.jpg"
    img_path = Path(img_path)

    data_path = sys.argv[2] if len(sys.argv) > 2 else "data/France"
    data_path = Path(data_path)

    # results = knn_query(img_path, 10)
    results = knn_query(img_path, 10, data_path)

    for name, similarity in results:
        print(f"{similarity:7.3f} % - {name} {'(identity)' if name == img_path else ''}")