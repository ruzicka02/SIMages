"""
Compute feature vectors from a directory of images using a CNN pre-trained on ImageNet dataset (VGG16 architecture).
Inspired by an article on medium.com

https://franky07724-57962.medium.com/using-keras-pre-trained-models-for-feature-extraction-in-image-clustering-a142c6cdf5b1
"""

import os
os.environ.setdefault("KERAS_BACKEND", "torch")  # Use PyTorch backend

import keras
import numpy as np
from pathlib import Path

def extract_img(model: keras.applications.vgg16.VGG16, img_path: Path) -> np.ndarray:
    """
    Using the given model, extract the features of the loaded image. Return them in a single np vector.
    """
    img = keras.utils.load_img(img_path, target_size=(224, 224))
    img_data = keras.utils.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)  # 0-th dimension... batch size (1)
    img_data = keras.applications.vgg16.preprocess_input(img_data)

    return model.predict(img_data).flatten()


def extract_dir(dir_path: Path) -> tuple[np.ndarray, list[str]]:
    """
    Open a directory of images, load them and extract their features. Store these features in a single array.
    Using the VGG16 model for feature extraction, the output shape will be (IMG_COUNT, 25088).

    TODO: This could be further optimized by performing the extraction in batches, instead of single images.
    However, this approach does not have to solve any excessive memory use when the image count is higher.
    """
    model = keras.applications.vgg16.VGG16(weights='imagenet', include_top=False)  # without the final fc layer + softmax
    img_order = []
    feats = []

    for img in dir_path.iterdir():
        if img.suffix in [".png", ".jpg", ".jpeg"]:  # other formats are probably also compatible
            print(img)
            img_order.append(img.name)  # only the file name, assumes the dir path knowledge
            feats.append(extract_img(model, img))

    feat_array = np.array(feats)  # highest axis... individual images
    return feat_array, img_order

if __name__ == "__main__":
    features, img_order = extract_dir(Path("data"))
    # print(feat.shape)
    np.save("data/features.npy", features)

    with open("data/img_order.txt", "w") as f:
        for img in img_order:
            f.write(f"{img}\n")