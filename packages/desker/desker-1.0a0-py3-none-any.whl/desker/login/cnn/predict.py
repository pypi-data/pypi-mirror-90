#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: asr
"""

import os
from typing import Optional

from typing import Optional

import numpy as np
from PIL.Image import Image as ImageType

from desker.login.cnn.train import Net, __default_device__

# global variable model (private)
__model__: Net = None


def load_model(path: Optional[str] = None, device: str = __default_device__):
    """
    Load the default module model

    Parameters
    ----------
    path: str
        CNN model to load
    device : str, optional
        Device where the model is stored ('cpu' or 'cuda')
    """
    if path is None:
        folder = os.path.dirname(__file__)
        path = os.path.join(folder, "model.cnn")
    global __model__
    __model__ = Net.from_model(path)
    __model__ = __model__.to(device)


def login_page_probability(image: ImageType,
                           model: Optional[Net] = None) -> float:
    """
    Returns the probability of a screenshot to be classified
    as a login page.

    Parameters
    ----------
    image : PIL.Image.Image
        screenshot
    model : Net, optional
        CNN model to use (see desker.login.cnn.train.Net)
        It uses the default module model if not provided but you must
        ensure that it is well imported (see load_model).

    Returns
    -------
    float
        Probability to be classified as a login page (between 0 and 1)
    """
    model = model if model else __model__
    if model is None:
        raise ValueError(
            "Default model is not loaded, "
            "you must either load it or "
            "provide a custom one")

    scores = model.raw_score_single_image(image)
    # softmax
    softmax = np.exp(scores)
    return softmax[1] / softmax.sum()


def is_login_page(image: ImageType, model: Optional[Net] = None) -> bool:
    """
    Detect if a screenshot corresponds to a login page

    Parameters
    ----------
    image : PIL.Image.Image
        input image
    model : Net, optional
        CNN model to use (see desker.login.cnn.train.Net)
        It uses the default module model if not provided but you must
        ensure that it is well imported (see load_model).

    Returns
    -------
    bool
        True if the image looks like a login page
    """
    model = model if model else __model__
    if model is None:
        raise ValueError(
            "Default model is not loaded, "
            "you must either load it or "
            "provide a custom one")

    label = model.predict_single_image(image)
    return label == 1
