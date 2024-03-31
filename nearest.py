"""
Using precomputed weights, find the closest photos to a photo.
"""

import numpy as np
from pathlib import Path
import sys

from utils import chdir

def _prepare_query(img: Path, metric: str = "cos", query_data: Path | None = None) -> tuple[list[Path], list[float]]:
    chdir()

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

    assert metric in ["cos", "euclid"], "Invalid metric given."
    if metric == "cos":
        # cosine (dot-product) similarity... higher is better
        # relative to the maximum value (exact match)
        img_norm = np.linalg.norm(img_features)
        sims = [np.dot(img_features, feats[i]) / img_norm / np.linalg.norm(feats[i]) for i in range(imgs)]
    elif metric == "euclid":
        # here, sims actually represent distances, not similarities
        # sacrifices in naming conventions had to be made, i guess
        sims = [np.linalg.norm(img_features - feats[i]) for i in range(imgs)]

    return names, sims


def knn_query(img: Path, metric: str, k: int, query_data: Path | None = None, verbose: bool = False) -> list[tuple[Path, float]]:
    """
    Select k items from query_data directory most similar to img. When query_data is not given,
    assume the parent directory of img (self-join).
    """
    names, sims = _prepare_query(img, metric, query_data)

    assert metric in ["cos", "euclid"], "Invalid metric given."
    res_step = -1 if metric == "cos" else 1  # order desc for similarity (higher is better), asc for distance
    res_limit = -k - 1 if metric == "cos" else k

    result = []
    for s in sorted(sims)[:res_limit:res_step]:  # top k
        name = names[np.where(sims == s)[0][0]]
        result.append((Path(query_data / name), 100 * s))

    if verbose:
        for name, similarity in result:
            print(f"{similarity:7.3f} % - {name} {'(identity)' if name == img else ''}")

    return result

    # time benchmark - entire similarity matrix
    # np.array([[np.dot(feats[i], feats[j]) for i in range(imgs)] for j in range(imgs)])


def range_query(img: Path, metric: str, threshold: float, query_data: Path | None = None, verbose: bool = False) -> list[tuple[Path, float]]:
    """
    Select k items from query_data directory most similar to img. When query_data is not given,
    assume the parent directory of img (self-join).
    """
    names, sims = _prepare_query(img, metric, query_data)

    # obtain correct k, then perform kNN once again
    sims_array = np.array(sims)
    print(threshold)
    print(sims_array)

    assert metric in ["cos", "euclid"], "Invalid metric given."
    k = len(sims_array[sims_array > threshold]) if metric == "cos" else len(sims_array[sims_array < threshold])

    res_step = -1 if metric == "cos" else 1
    res_limit = -k - 1 if metric == "cos" else k

    result = []
    for s in sorted(sims)[:res_limit:res_step]:
        name = names[np.where(sims == s)[0][0]]
        result.append((Path(query_data / name), 100 * s if metric == "cos" else s))

    if verbose:
        for name, similarity in result:
            print(f"{similarity:7.3f} % - {name} {'(identity)' if name == img else ''}")

    return result

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "data/Italy/IMG20230803112016.jpg"
    img_path = Path(img_path)

    data_path = sys.argv[2] if len(sys.argv) > 2 else "data/France"
    data_path = Path(data_path)

    # results = knn_query(img_path, 10)
    result = knn_query(img_path, 10, data_path, verbose=True)
