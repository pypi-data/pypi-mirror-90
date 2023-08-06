#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: asr
"""

import os
from functools import wraps
from typing import Callable, Dict, Optional

import joblib
import numpy as np
import pandas as pd
from PIL import Image
from PIL.Image import Image as ImageType
from sklearn.neighbors import KNeighborsClassifier as KNN

# global variable model (private)
__model__ = None

# global hard-coded threshold for login page
# detection
__max_dist_threshold__ = 4.0


def use_global_model_if_not_provided(f: Callable) -> Callable:
    """
    Basic decorator to set the model as the default model
    if the latter is not provided (i.e. 'model = None')
    """
    @wraps(f)
    def new(*args, **kwargs):
        kwargs.setdefault("model", __model__)
        return f(*args, **kwargs)
    return new


def import_model(file: Optional[str] = None) -> None:
    """
    Import the KNN model as a global object into
    the login sub-library.

    Parameters
    ----------
    file : str
        Path to the pickled model. If not given, it takes the
        file model.knn in the desker/login/ directory.
    """
    global __model__
    if file is None:
        file = os.path.join(os.path.dirname(__file__), "model.knn")
    __model__ = load(file)


def crop(M: np.ndarray) -> ImageType:
    """
    Returns an image where without black borders
    """
    Z = (M[:, :, 0] == 0) & (M[:, :, 1] == 0) & (M[:, :, 2] == 0)
    cols = Z.all(axis=0)
    rows = Z.all(axis=1)
    return Image.fromarray(M[:, ~cols, :][~rows, :, :])


def image_to_features(img: ImageType) -> np.ndarray:
    """
    Compute the features of an image
    """
    d = image_to_feature_dict(img)
    # it must be sorted to ensure that values
    # are in the right order
    return np.asarray([[d[k] for k in sorted(d.keys())]])


def image_to_feature_dict(img: ImageType) -> dict:
    """
    Compute feature from image. This function
    is very important since all other feature extraction
    processes  are based on it.
    """
    img_cropped = crop(np.asarray(img))
    # legacy fields
    features = {
        "R": np.mean(img_cropped.getchannel("R")),
        "G": np.mean(img_cropped.getchannel("G")),
        "B": np.mean(img_cropped.getchannel("B")),
        # "entropy": img_cropped.entropy(),
    }

    proba = np.arange(10, 100, 10)
    for channel in "RGB":
        dist = np.asarray(img_cropped.getchannel(channel)).flatten()
        p = np.percentile(dist, proba)
        for i, q in enumerate(proba):
            key = "{:s}{:d}".format(channel, q)
            features[key] = p[i]
    return features


def load_data(P: pd.DataFrame, base_dir: str) -> pd.DataFrame:
    records = []
    for index, row in P.iterrows():
        label = row.label
        file = os.path.join(base_dir, row.img)
        img = Image.open(file)
        d = image_to_feature_dict(img)
        d["label"] = label
        d["path"] = file
        records.append(d)
    return pd.DataFrame(records)


def load(path: str) -> KNN:
    """
    Load a knn classifier from a file

    Parameters
    ----------
    path : str
        Path to the saved model
    """
    try:
        obj = joblib.load(path)
    except BaseException as err:
        raise Exception(f"Error while loading model from {path}: {err}")
    if isinstance(obj, KNN):
        return obj
    raise ImportError(
        "Bad object loaded (expect 'KNN',"
        " got '{}')".format(type(obj)))


@use_global_model_if_not_provided
def predict_from_image(img: ImageType,
                       model: Optional[KNN] = None) -> str:
    """
    Returns the closest OS

    Parameters
    ----------
    img : PIL.Image.Image
        input image
    model : sklearn.neighbors.KNeighborsClassifier
        the KNN model to use. It uses the globally
        loaded model if not provided.
    """
    X = image_to_features(img)
    return model.predict(X)[0]


@use_global_model_if_not_provided
def predict_proba_from_image(img: ImageType,
                             model: Optional[KNN] = None) -> Dict[str, float]:
    """
    Returns the prediction probabilities

    Parameters
    ----------
    img : PIL.Image.Image
        input image
    model : sklearn.neighbors.KNeighborsClassifier
        the KNN model to use. It uses the globally
        loaded model if not provided.
    """
    X = image_to_features(img)
    return dict(zip(sorted(model.classes_), model.predict_proba(X)[0]))


def predict_from_file(img_file: str,
                      model: Optional[KNN] = None) -> str:
    """
    Returns the nearest OS this image corresponds to

    Parameters
    ----------
    img_file : str
        path to the image
    model : sklearn.neighbors.KNeighborsClassifier
        the KNN model to use. It uses the globally
        loaded model if not provided.
    """
    return predict_from_image(Image.open(img_file), model=model)


@use_global_model_if_not_provided
def get_distances(img: ImageType,
                  model: Optional[KNN] = None) -> np.ndarray:
    """
    Compute the distances between the image and the
    nearest neighbors

    Parameters
    ----------
    img : PIL.Image.Image
        input image
    model : sklearn.neighbors.KNeighborsClassifier
        the KNN model to use. It uses the globally
        loaded model if not provided.
    """
    X = image_to_features(img)
    dist, _ = model.kneighbors(X, n_neighbors=len(model.classes_),
                               return_distance=True)
    return dist[0]


def is_login_page(img: ImageType,
                  model: Optional[KNN] = None) -> bool:
    """
    Check if the input image looks like a screenshot

    Parameters
    ----------
    img : PIL.Image.Image
        input image
    model : sklearn.neighbors.KNeighborsClassifier
        the KNN model to use. It uses the globally
        loaded model if not provided.
    """
    dist = get_distances(img, model)
    if dist < __max_dist_threshold__:
        return True
    return False
