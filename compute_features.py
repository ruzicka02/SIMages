"""
Compute feature vectors from a directory of images using a CNN pre-trained on ImageNet dataset (VGG16 architecture).
Inspired by an article on medium.com

https://franky07724-57962.medium.com/using-keras-pre-trained-models-for-feature-extraction-in-image-clustering-a142c6cdf5b1
"""

import sys
import os
os.environ.setdefault("KERAS_BACKEND", "torch")  # Use PyTorch backend

import keras
from keras.applications import vgg16
import numpy as np
from pathlib import Path

# parameter of the vgg16 model, 7 * 7 * 512
FEATURE_SIZE = 25088
# other formats are probably also compatible
SUPPORTED_IMG = [".png", ".jpg", ".jpeg"]

def extract_batch(model: vgg16.VGG16, img_paths: list[Path]) -> np.ndarray:
    """
    Using the given model, extract the features of the loaded image. Return them in a numpy array
    of shape (BATCH_SIZE, 25088).
    """
    batch_array = np.ndarray((len(img_paths), 224, 224, 3), dtype=np.float32)
    i = 0
    for p in img_paths:
        img = keras.utils.load_img(p, target_size=(224, 224))
        batch_array[i] = keras.utils.img_to_array(img)
        i += 1

    # add 0-th dimension... only when batch size is (implicit) 1
    # img_data = np.expand_dims(img_data, axis=0)
    batch_array = vgg16.preprocess_input(batch_array)
    batch_array = model.predict(batch_array)
    return batch_array.reshape(batch_array.shape[0], -1)  # keep 1st dimension (images), flatten the rest


def extract_dir(dir_path: Path) -> tuple[np.ndarray, list[str]]:
    """
    Open a directory of images, load them and extract their features. Store these features in a single array.
    Using the VGG16 model for feature extraction, the output shape will be (IMG_COUNT, 25088).

    This is further optimized by performing the extraction in batches, instead of single images.
    Batch size is fixed to 64 to solve any excessive memory use when the image count is higher.
    """
    model = vgg16.VGG16(weights='imagenet', include_top=False)  # without the final fc layer + softmax
    img_order = []
    feats = []

    loaded = 0
    img_to_load = []
    for img in dir_path.iterdir():
        if img.suffix in SUPPORTED_IMG:
            # print(img)
            img_order.append(img.name)  # only the file name, assumes the dir path knowledge
            img_to_load.append(img)  # full name, for image loading and processing

            # process one batch
            if len(img_order) % 64 == 0:
                feats.append(extract_batch(model, img_to_load))
                loaded += len(img_to_load)
                print(f"Loaded: {loaded}")
                img_to_load = []

    # remaining (smaller batch)
    if img_to_load != []:
        feats.append(extract_batch(model, img_to_load))
        loaded += len(img_to_load)
        print(f"Loaded: {loaded}")

    if len(feats) == 0:
        print(f"Directory {dir_path} does not contain any supported pictures!")
        sys.exit(1)

    feat_array = np.concatenate(feats, axis=0)  # highest axis... individual images
    return feat_array, img_order

def compute_features(dir_path: Path) -> None:
    """Computes the features and writes them into the features.npz file."""
    features, img_order = extract_dir(dir_path)
    # print(features.shape)
    # np.savez(dir_path / "features_uncompressed.npz", features)
    np.savez_compressed(dir_path / "features.npz", features)

    with open(dir_path / "img_order.txt", "w") as f:
        print(*img_order, sep='\n', file=f)

def check_features(dir_path: Path) -> None:
    """
    Checks whether the features and order file are present in the directory.
    Also checks whether new files were also added to the directory by comparing lengths.
    If not, they are computed and written into the files.
    """
    if not (dir_path / "img_order.txt").exists() or not (dir_path / "features.npz").exists():
        print(f"Something is missing -- (re)computing features for {dir_path}")
        compute_features(dir_path)


    with open(dir_path / "img_order.txt", 'r') as f:
        img_order_lines = {l.strip() for l in f}

    imgs_present = {x.name for x in dir_path.glob("*") if x.suffix in SUPPORTED_IMG}

    if img_order_lines.symmetric_difference(imgs_present) != set():
        print(f"Files in the directory changed ({len(img_order_lines) = }, {len(imgs_present) = }, "
              f"symm_diff {img_order_lines.symmetric_difference(imgs_present)}) -- (re)computing features for {dir_path}")
        compute_features(dir_path)

if __name__ == "__main__":
    dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    compute_features(Path(dir))
