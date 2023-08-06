# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 14:10:51 2020

@author: jpd
"""

import json
import os
from typing import Callable, List, Optional, Tuple

import numpy as np
import torch
from PIL import Image

import desker.faster_rcnn.transforms as T

# =============================================================================
# La fonction get_annotations permet d'obtenir les "attributes" (dans notre
# cas les dossiers) à partir du fichier json
# =============================================================================


# def get_annotations(json_dict: dict) -> Tuple[np.ndarray, np.ndarray]:
#     """Créer une liste qui contient toutes les
#     annotations rectangulaires d'une image
#     """
#     click_zones = []
#     label = []
#     if len(json_dict['regions']) == 0:
#         return np.array([[]]), np.array([])
#     for annotation in json_dict['regions']:
#         shape_attributes = annotation['shape_attributes']
#         region_attributes = annotation['region_attributes']
#         x1 = shape_attributes['x']
#         y1 = shape_attributes['y']
#         x2 = x1 + shape_attributes['width']
#         y2 = y1 + shape_attributes['height']
#         click_zones.append([x1, y1, x2, y2])
#         label.append(region_attributes['Icon'])
#     label = [label_dict[x] for x in label]
#     return [np.array(click_zones), np.array(label)]

# =============================================================================
# La classe ScreenDataset permet de d'utiliser une base de données
# personnalisée. Elle contient les méthodes __getitem__ et __len__ comme
# indiqué sur la documentation de PyTorch
# =============================================================================


class ScreenDataset(object):
    """
    Attributes
    ----------

    json : dict
        The python representation of the json file (annotation file)
    root : str
        Directory of the images

    """
    __extensions__ = ['png', 'jpg', 'jpeg', 'bmp']

    def __init__(self,
                 root: Optional[str] = None,
                 json_file: Optional[str] = None,
                 transforms: Optional[Callable] = None,
                 detect: bool = False):
        """
        Parameters
        ----------
        root : str
            Path to the file folder. If it is not given, the root path is
            guessed from the json file
        json_file : str
            Path to the VIA annotations file (json file)
        transforms : Callable
            Function to transform the PIL images
        detect : bool
            If True, it does not return labels
        """
        if root is None and json_file is None:
            raise ValueError(
                "Provide either an image directory "
                "or an annotation file (json_file)")

        self.transforms = transforms

        # only a root directory is given
        if json_file is None:
            self.root = root
            self.json = self.__init_fake_json()
            self.detect = True
            self.labels = None
            return

        # the json file contains everything
        self.json = json.load(open(json_file, 'r'))

        # get the root from the json file
        root = os.path.join(
            os.path.dirname(json_file),
            self.json['_via_settings']['core']['default_filepath'])
        self.root = os.path.normpath(root)

        self.detect = detect

        # only get the annotated images (this list does not contain the real
        # name of the images).
        # You must invoke self.json["_via_img_metadata"][img_name]['filename']
        self.imgs = self.json['_via_image_id_list']

        # the first id (0) does not define a class (background)
        self.labels = ['not_defined'] + self.__get_labels()

    def __get_images(self) -> List[str]:
        imgs = []
        for f in sorted(os.listdir(self.root)):
            for ext in self.__extensions__:
                if f.lower().endswith(ext):
                    imgs.append(f)
        return imgs

    def __init_fake_json(self):
        imgs = self.__get_images()
        self.json = {
            "_via_settings": {},
            "_via_attributes": {},
            "_via_data_format_version": "",
            "_via_image_id_list": imgs,
            "_via_img_metadata": dict((f, {'filename': f}) for f in imgs)
        }

    def __get_labels(self) -> List[str]:
        """
        This function returns all the different labels
        of the dataset from the .json file
        It returns the sorted list of the labels
        """
        return sorted(self.json["_via_attributes"]
                      ["region"]["Icon"]["options"].keys())

    def __get_annotations(
            self, via_image_name: str) -> Tuple[np.ndarray, np.ndarray]:
        attr = self.json["_via_img_metadata"][via_image_name]
        boxes = []
        labels = []
        for r in attr['regions']:
            shape_attributes = r['shape_attributes']
            region_attributes = r['region_attributes']
            x1 = shape_attributes['x']
            y1 = shape_attributes['y']
            x2 = x1 + shape_attributes['width']
            y2 = y1 + shape_attributes['height']
            boxes.append([x1, y1, x2, y2])
            labels.append(region_attributes['Icon'])
        return np.array(boxes), np.fromiter(
            [self.labels.index(lab) for lab in labels], dtype=int)

    def __getitem__(self, idx):
        # load images ad masks
        via_img_name = self.imgs[idx]
        img_name = self.json["_via_img_metadata"][via_img_name]['filename']
        img_path = os.path.join(self.root, img_name)
        if self.detect:
            if self.transforms is not None:
                return self.transforms(Image.open(img_path).convert("RGB"), {})
            else:
                return Image.open(img_path).convert("RGB"), {}

        img = Image.open(img_path).convert("RGB")
        boxes, labels = self.__get_annotations(via_img_name)

        num_objs = len(boxes)

        if len(boxes[0]) == 0:
            area = np.array([0])
        else:
            area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])

        # suppose all instances are not crowd
        target = {
            "boxes": torch.as_tensor(boxes, dtype=torch.float32),
            "labels": torch.tensor(labels, dtype=torch.int64),
            "image_id": torch.tensor([idx], dtype=torch.uint8),
            "area": torch.as_tensor(area, dtype=torch.int32),
            "iscrowd": torch.zeros((num_objs,), dtype=torch.int64),
        }

        if self.transforms is not None:
            img, target = self.transforms(img, target)
        return img, target

    def __len__(self):
        return len(self.imgs)

    def nb_classes(self) -> int:
        """
        Return the number of classes
        (the background is included)
        """
        return len(self.labels)

    def save_labels(self, path: Optional[str] = None) -> None:
        """
        Save the labels as a json file

        Parameters
        ----------
        path : str, optional
            Path to the json file. It saves in the current
            directory as labels.json if it is not provided
        """
        if path is None:
            folder = os.path.dirname(__file__)
            path = os.path.join(folder, "labels.json")
        with open(path, 'w') as w:
            labels = ["background"] + self.__get_labels()
            m = zip(range(len(labels)), labels)
            json.dump(dict(m), w, indent=4)


# It must be acknoledged that with some information is lost: for instance, the model can no longer tell apart a forward and a backward arrow
def get_transform(train: bool) -> Callable:
    transforms = []
    # converts the image, a PIL image, into a PyTorch Tensor
    transforms.append(T.ToTensor())
    if train:
        # during training, randomly flip the training images
        # and ground-truth for data augmentation
        transforms.append(T.RandomHorizontalFlip(0.5))
        transforms.append(T.RandomVerticalFlip(0.5))
    return T.Compose(transforms)
