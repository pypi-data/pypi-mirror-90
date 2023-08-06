#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 15:46:48 2020

@author: jpd
"""
import json
import os
from typing import Dict, Optional

import numpy as np
import pandas as pd
import torch
from PIL import ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.transforms import functional as F

from desker.faster_rcnn import utils
from desker.faster_rcnn.train import get_FasterRCNN_model

device = (
    torch.device("cuda") if torch.cuda.is_available(
    ) else torch.device("cpu")
)

# Default model
__model__: FasterRCNN = None  # model not defined

# Default dictionnary. It maps the
# class id to the class names
__classes__: Dict[int, str] = {}


def load_model(
        model_file: Optional[str] = None,
        class_file: Optional[str] = None,
        nb_labels: Optional[int] = None):
    """
    Load a FasterRCNN model

    Parameters
    ----------
    model_file: str, optional
        Path to the FasterRCNN model to load. It looks for 'model.frcnn'
        within this file folder if it is not provided
    class_file: str, optional
        Path to a json file providing a map class_id -> class_name. It is
        required for prediction.
    nb_labels: int, optional
        Number of classes (for model training especially)

    Raises
    ------
    ValueError
        If neither class_file nor nb_labels are defined
    """
    global __model__
    global __classes__

    # directory of this file
    wd = os.path.dirname(__file__)

    # default model
    if model_file is None:
        model_file = os.path.join(wd, "model.frcnn")

    if class_file is None:
        class_file = os.path.join(wd, "labels.json")

    if (nb_labels is None) and (class_file is None):
        raise ValueError(
            "You must define either num_labels (training) "
            "or class_file (prediction)")

    if nb_labels is None:
        with open(class_file, 'r') as js:
            # define the class dict
            __classes__ = json.loads(js.read())
            nb_labels = len(__classes__.keys())

    # load en empty model
    __model__ = get_FasterRCNN_model(nb_labels)
    # update its parameters
    __model__.load_state_dict(torch.load(model_file))
    # prepare it
    __model__.to(device)
    __model__.eval()


def __overlap(box_a, box_b) -> bool:
    """
    Return True if the two boxes overlap
    """
    xa0, ya0, xa1, ya1 = box_a
    xb0, yb0, xb1, yb1 = box_b
    # x overlapping
    if xb0 > xa1 or xb1 < xa0:
        return False
    # y overlapping
    if ya0 > yb1 or ya1 < yb0:
        return False
    return True


def filter_pred(prediction: dict, threshold: float) -> dict:
    """
    Filters a prediction by rremoving predictions with a confidence score
    lower than the threshold. In addition, it removes overlapping
    boxes and select the one with highest score.

    Parameters
    ----------
    prediction : dict
        Prediction to be filtered.
    threshold: float
        Minimum confidence score required.
    """
    boxes = np.array(prediction["boxes"])
    labels = np.array(prediction["labels"])
    conf_scores = np.array(prediction["scores"])
    output = {
        "boxes": boxes[conf_scores > threshold],
        "labels": labels[conf_scores > threshold],
        "scores": conf_scores[conf_scores > threshold],
    }

    filtered_output = {
        "boxes": [],
        "labels": [],
        "scores": [],
    }
    # remove overlapping predictions
    for box_a, label, score in zip(
            output["boxes"],
            output["labels"],
            output["scores"]):
        try:
            for box_b in filtered_output["boxes"]:
                if __overlap(box_a, box_b):
                    raise Exception
            filtered_output["boxes"].append(box_a.tolist())
            filtered_output["labels"].append(label)
            filtered_output["scores"].append(score)
        except Exception:
            pass

    return filtered_output
    # return output


def draw_boxes(img: ImageType, prediction: dict) -> ImageType:
    """ Visualisation tool
    """

    labels = np.array(prediction["labels"])
    boxes = np.array(prediction["boxes"])
    scores = np.array(prediction["scores"])
    try:
        font = ImageFont.truetype(
            "dejavu/DejaVuSans.ttf")
    except OSError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    nb_colors = len(utils.circular_colors)
    for i, label in enumerate(labels):
        color = tuple(int(255 * c)
                      for c in utils.circular_colors[i % nb_colors])
        lab_boxes = boxes[(labels == label)]
        lab_scores = scores[(labels == label)]
        for box, score in zip(lab_boxes, lab_scores):
            # default config
            # position: inside the box by defaults
            config = {
                "xy": (box[0], box[1]),
                "text": f"{label} ({score:.2f})",
                "font": font,
                "anchor": "la",
                "align": "left", }
            # draw the bounding box
            draw.rectangle(list(box), outline=color, width=4)
            # specific config for some buttons
            if 'close' in label:
                config["anchor"] = "rb"
                config["xy"] = (box[2], box[1])
            elif 'zoom' in label:
                config["xy"] = (box[0], box[3])
                config["anchor"] = "lt"
            elif 'minimize' in label:
                config["xy"] = (box[2], box[3])
                config["anchor"] = "rt"

            # estimate the bounding box of the text
            text_box = draw.textbbox(**config)
            # fill it with white first
            draw.rectangle(text_box, fill=(255, 255, 255))
            # write text
            draw.text(**config, fill=color)
    return img


def predict_elements_demo(image: ImageType,
                          model: FasterRCNN = __model__,
                          threshold: float = 0.0) -> ImageType:
    """
    This function returns the input image annotated with the
    elements discovered. Overlapping elements are removed,
    and you can tweak the threshold to keep only elements
    with high score.

    Parameters
    ----------
    image : PIL.Image.Image
        Screenshot on which prediction will be performed
    model : FasterRCNN
        FasterRCNN model to use for the inference
    threshold : float
        Score threshold (between 0. and 1.)
    """
    pred = predict_elements(image, model)
    # null threshold means that only the overlapping
    # bounding boxes are removed
    pred = filter_pred(pred, threshold)
    # draw boxes
    return draw_boxes(image, pred)


def transform_image(infile: ImageType):
    input_tensor = F.to_tensor(infile).unsqueeze_(0)
    return input_tensor


def predict_elements(image: ImageType,
                     model: FasterRCNN = __model__,
                     filter_predictions: bool = False,
                     threshold: float = 0.0) -> dict:
    """
    Predicts all kinds of icons on a screenshot

    Parameters
    ----------
    image : PIL.Image.Image
        Screenshot on which prediction will be performed
    model: FasterRCNN
        FasterRCNN model to use for the inference
    filter_predictions : bool
        Remove overlapping boxes (keep the best) and apply
        the given threshold to prune worst boxes.
    threshold : float
        Score threshold (between 0. and 1.)

    Returns
    -------
    dict
        labels: list of integers corresponding to the label of the
                predictions,
        boxes: list of arrays containg the bounding boxes of the
               predicted objects
        scores: list of floats assessing the confidence of the model in
                each prediction
    """
    global __classes__

    if __model__ is None:
        raise Exception("No model loaded")
    input_tensor = transform_image(image)
    with torch.no_grad():
        prediction = __model__(input_tensor.to(device))

    # prediction is a list
    # (the model is supposed to be fed with a batch)
    prediction = prediction[0]

    labels = [__classes__[str(k)]
              for k in prediction["labels"].to("cpu").tolist()]
    boxes = prediction["boxes"].to("cpu").tolist()
    scores = prediction["scores"].to("cpu").tolist()

    pred = {
        "boxes": boxes,
        "scores": scores,
        "labels": labels}
    if filter_pred:
        return filter_pred(pred, threshold)
    return pred


def predict_single(image: ImageType,
                   label: str,
                   model: FasterRCNN = __model__) -> dict:
    """
    Predicts only a single kind of object on a screenshot

    Parameters
    ----------
    image : PIL.Image.Image
        Screenshot on which prediction will be performed
    label: str
        object to predict
    model: FasterRCNN
        FasterRCNN model to use for the inference

    Returns
    -------
    dict
        boxes: list of arrays containg the bounding boxes of the
               predicted objects
        scores: list of floats assessing the confidence of the model in
                each prediction
    """
    P = pd.DataFrame(predict_elements(image, model))
    F = P[["boxes", "scores"]][P["labels"] == label]
    return F.to_dict(orient="list")
