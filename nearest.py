"""
Using precomputed weights, find the closest photos to a photo.
"""

import numpy as np
import sys
# from pathlib import Path

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "IMG20230803112016.jpg"

    feats = np.load("data/features.npz")['arr_0']  # selection from "archive" needed for npz
    imgs = feats.shape[0]

    print(f"{imgs} images loaded")

    with open("data/img_order.txt", "r") as f:
        names = f.read().split()
    assert imgs == len(names), "Mismatch detected between the image names and feature matrix."

    img_index = names.index(img_path)

    # cosine (dot-product) similarity... higher is better
    sims = [np.dot(feats[img_index], feats[i]) for i in range(imgs)]
    sims /= sims[img_index]  # relative to the maximum value (exact match)

    k = 10
    for s in sorted(sims)[:-k-1:-1]:  # top 10, reversed (higher is better)
        name = names[np.where(sims == s)[0][0]]
        print(f"{100 * s:7.3f} % - {name} {'(identity)' if name == img_path else ''}")

    # time benchmark - similarity matrix
    # np.array([[np.dot(feats[i], feats[j]) for i in range(imgs)] for j in range(imgs)])