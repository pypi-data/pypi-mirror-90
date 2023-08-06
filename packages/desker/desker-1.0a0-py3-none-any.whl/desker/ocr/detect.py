#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:13:29 2020

@author: jpd
"""

from typing import Callable, List, Tuple, Union

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageColor
from PIL.Image import Image as ImageType
from pytesseract import Output
from sklearn.cluster import KMeans

Box = Tuple[int, int, int, int]
BoxFilter = Callable[[Box], bool]


def get_text(tessdict: dict) -> dict:
    """ clears tesserat output from empty elements
    """
    txt = np.array(tessdict['text'])
    boxes = np.array([
        tessdict['left'],
        tessdict['top'],
        tessdict['width'],
        tessdict['height']], dtype=int)
    mask = [len(x) > 3 for x in txt]
    boxes = boxes[:, mask]
    txt = txt[mask]
    new_boxes = np.array([boxes[0, :],
                          boxes[1, :],
                          boxes[0, :] + boxes[2, :],
                          boxes[1, :] + boxes[3, :]])
    output_dict = {}
    for i, word in enumerate(txt):
        if word in output_dict.keys():
            output_dict[word].append(new_boxes.T[i].tolist())
        else:
            output_dict[word] = [new_boxes.T[i].tolist()]
    return output_dict


def get_boxes(
        img: ImageType,
        custom_config: str = r'-l fra+eng --psm 4') -> dict:
    tessdict = pytesseract.image_to_data(img,
                                         output_type=Output.DICT,
                                         config=custom_config)
    return get_text(tessdict)


def get_text_under_boxes(
        img: ImageType,
        boxes: List[Box],
        config: str = r'-l fra+eng --psm 6') -> dict:
    """Detects text under boxes

    Parameters
    ----------
    img : PIL.Image.Image
        Input image
    boxes: List[Box]
        List of boxes to inspect.

    Notes
    -----
    --psm 7 = Treat the image as a single text line.
    """
    # output = {}
    below_boxes = []
    text = []
    for box in boxes:
        # below_box = [box[0] - 40, box[3] - 5, box[2] + 40, box[3] + 20]
        # below_box = (0.5 * (3 * box[0] - box[2]),
        #              box[3],
        #              0.5 * (3 * box[2] - box[0]),
        #              2 * box[3] - box[1])
        below_box = (2 * box[0] - box[2],
                     box[3],
                     2 * box[2] - box[0],
                     2 * box[3] - box[1])

        txt_box = img.crop(below_box)
        below_boxes.append(below_box)
        tessdict = pytesseract.image_to_data(txt_box,
                                             output_type=Output.DICT,
                                             config=config)

        max_conf = -1
        for conf, txt in zip(tessdict['conf'], tessdict['text']):
            if isinstance(conf, str) or conf < 50:
                continue
            if conf > max_conf:
                max_conf = conf
                candidate = txt
        if max_conf > 50:
            text.append(candidate)
        else:
            text.append(None)
    return text


# def get_img(img: Image):
#     '''detects image file on screen
#     --psm 11 = Sparse text. Find as much text as possible in no particular
#     order.
#     '''
#     txt_zones = get_boxes(img, custom_config=r'-l fra+eng --psm 11')
#     candidates = []
#     for name in txt_zones.keys():
#         if name.split('.')[-1] in ['png', 'jpeg', 'jpg']:
#             candidates.append(name)
#             print(candidates)
#     if len(candidates) > 0:
#         chosen_name = random.choice(candidates)
#         target = get_boxes_center(random.choice(txt_zones[chosen_name]))
#         return target
#     return None


def find_blocks(img: ImageType,
                min_occupation: float = 0.05,
                max_occupation: float = 0.95,
                min_aspect: float = 1 / 2,
                max_aspect: float = 2) -> (List[ImageType],
                                           List[np.ndarray]):
    """
    Find "relevant blocks" within an image, like paragraphs,
    side bars, banners etc.

    Parameters
    ----------
    img : PIL.Image.Image
        input image
    min_occupation : float
        Minimum surface of the windows in comparison to the whole image
    max_occupation : float
        Maximum surface of the windows in comparison to the whole image
    min_aspect : float
        Minimum ratio width/height
        It means that w/h > min_aspect
    max_aspect : float
        Maximum ratio width/height
        It means that w/h < max_aspect
    force_white_bg: bool
        Assume that the information is inside darker elements
        (example: bg is rather white and text is black)

    Returns
    -------
    sub_images : List[PIL.Image.Image]
        List of cropped images corresponding
        to the detected blocks
    masks : List[numpy.ndarray]
        List of mask corresponding to the areas
        of the detected blocks. The masks have
        the same size as the initial image
    """

    def is_box_valid(x: int, y: int, w: int, h: int) -> bool:
        return w * h > min_occupation * surface and w * h < max_occupation * \
            surface and w / h > min_aspect and w / h < max_aspect

    M = np.asarray(img)
    mask = np.zeros(M.shape[:2], dtype=np.bool)

    # gray image
    if len(M.shape) == 2:
        gray = M
    else:
        gray = cv2.cvtColor(M, cv2.COLOR_RGB2GRAY)

    # get the dominant color
    if gray.mean() < 255 / 2:
        th_type = cv2.THRESH_BINARY
    else:
        th_type = cv2.THRESH_BINARY_INV

    # Performing OTSU threshold
    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | th_type)

    # performig dilation
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    dilation = cv2.dilate(binary, rect_kernel, iterations=1)

    # Image.fromarray(dilation).show()
    # Image.fromarray(255 - dilation).show()
    # invert dilation image
    contours, _ = cv2.findContours(255 - dilation,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # keep only certain contours
    sub_images = []
    masks = []
    surface = np.prod(binary.size)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if is_box_valid(x, y, w, h):
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            mask = np.zeros(binary.shape, dtype=bool)
            mask[y:y + h, x:x + w] = True
            sub_images.append(img.crop((x, y, x + w, y + h)))
            masks.append(mask)

    return sub_images, masks


def detect_link_color(img: ImageType, q: float = 97.5) -> Tuple[str, float]:
    """
    Detect the colors of the links in a web page
    assuming they are rather blue

    Parameters
    ----------
    img : PIL.Image.Image
        Input image
    q : float
        Quantile to compute the decision thresholds. Valid pixels
        are the q% the closest of the found link color (within the
        "blue" cluster).
    """

    # find blocks of text
    # Not to be pollute by other images or banners...
    sub, masks = find_blocks(img, max_aspect=20.,
                             max_occupation=0.75,
                             min_occupation=0.025,
                             min_aspect=1 / 2)

    # merge all masks. It delimitates the
    # paragraphs
    mega_mask = np.sum(masks, axis=0, dtype=bool)

    # use a local copy
    X = np.copy(img)
    # work on text only (hide non paragraphs)
    X[~mega_mask, :] = (255, 255, 255)

    # here we remove pixels which have low chroma
    # it means that they are either white or black
    # (no chroma)
    H = cv2.cvtColor(X, cv2.COLOR_RGB2HSV_FULL)
    chroma = (H[:, :, 1] / 255.) * (H[:, :, 2] / 255.)
    mask = chroma > 0.35
    X[~mask, :] = (255, 255, 255)

    # -- debug --
    # Image.fromarray(X).show()

    # filter the aforementionned pixels
    X = X[mega_mask & mask]

    # Pixel clustering
    # KMeans init
    centers = np.array([
        (0, 0, 0),  #  black
        (255, 255, 255),  # white
        (0, 0, 255),  # blue (class = 2)
    ])
    k = centers.shape[0]
    km = KMeans(n_clusters=k, init=centers, n_init=1)
    km.fit(X)

    # Get pixels of the "blue" cluster
    blue_like_pixels = X[km.labels_ == 2]
    # mean blue
    blue = [int(round(c)) for c in km.cluster_centers_[2]]
    # distance to the mean
    squared_distance = (
        (blue_like_pixels - km.cluster_centers_[2])**2).sum(1).flatten()
    # return the color and the 97.5% percentile distance
    return tuple(blue), np.percentile(squared_distance, q)


def get_links(img: ImageType,
              link_colors: Union[str, List[str]] = ["#0645AD"],
              result: str = "centers",
              min_confidence: int = 0) -> Union[
                  List[Tuple[str, int, int]],
                  List[Tuple[str, int, int, int, int]]]:
    """Return the links on a webpage given the font color

    Parameters
    ----------
    img : PIL.Image.Image
        Pillow image (the screenshot)
    link_colors : List[str]
        List of colors taken into account (HTML format).
        Set "auto" to launch the color detection engine.
    result : str
        result type (either "boxes" : (text, top, left, height, width)
        or "centers" [default] : (text, x, y))
    min_confidence : int
        Tesseract confidence threshold
    """

    # hardcoded threshold on squared distance from the
    # the mean color
    th = 12000

    # auto mode
    # the color and the threshold are
    # automatically found
    if link_colors == "auto":
        color, th = detect_link_color(img, 93.5)
        link_colors = [color]

    if isinstance(link_colors, (str, tuple)):
        link_colors = [link_colors]

    # normalize colors
    colors = [
        ImageColor.getcolor(
            c, "RGB") if isinstance(
            c, str) else c for c in link_colors]

    M = np.copy(img.convert("RGB"))
    # init a null mask (False)
    mask = np.zeros(M.shape[:2], dtype=bool)
    for c in colors:
        W = np.tensordot(np.ones(M.shape[:2]), c, 0)
        D = np.sum((W - M)**2, axis=2)
        # keep pixels which are not to far from the
        # given ones. Here we use a hardcoded threshold
        # maybe it can be given in parameters but it has
        # not a real sense. In the auto mode, the threshold
        # is given as a 97.5 percentile.
        mask = mask | (D < th)
    # set unmasked pixels to white
    M[~mask, :] = 255

    # go tesseract
    data = pytesseract.image_to_data(Image.fromarray(M),
                                     lang="fra+eng",
                                     output_type=Output.DATAFRAME,
                                     pandas_config={"keep_default_na": False})
    # clean empty text
    data["text"] = data["text"].apply(lambda x: x.strip())
    # keep only when we are confident
    P = data[(data["conf"] >= min_confidence) & (data["text"] != "")]
    # return the desired result
    if result == "boxes":
        cols = ["top", "left", "height", "width", "text"]
        return P[cols].to_records(index=False).tolist()
    return list(zip(P["text"],
                    P["left"] + P["width"] / 2,
                    P["top"] + P["height"] / 2))


def get_emails(img_input: ImageType) -> str:
    """
    Identify the sender of an email

    Parameters
    ----------
    img : PIL.Image.Image
        Pillow image (the screenshot)
    result : str
        email address
    """

    # the account's email address is usually displayed in the upper bar, to
    # pevent from choosing this address, the image is cropped
    img_input = img_input.crop([0, 50, 1920, 1080])
    # look for any "@" in the image so as to make a zoom on the "To/From/Cc
    # zone"
    txt_samples = get_boxes(img_input, r'-l fra+eng --psm 6')
    to_from_cc = []
    for sample in txt_samples.keys():
        if sample.find('@') != -1:
            zone = txt_samples[sample][0]
            x = (zone[2] + zone[0]) / 2
            y = (zone[3] + zone[1]) / 2
            to_from_cc.append(np.array([x, y]))
    # choose an email address located in the upper part of the image
    top_address = to_from_cc[np.argmin(np.array(to_from_cc)[:, 1])]
    x, y = top_address[0], top_address[1]
    # select a box that covers the "To/From/Cc zone" and crop it
    box = [max(x - 400, 0), max(y - 80, 0),
           min(x + 500, 1920), min(y + 150, 1080)]
    addressee_zone = img_input.crop(box)
    addressee_zone.save("crop_zone.png")
    addresses = get_boxes(addressee_zone, r'-l fra+eng --psm 6')
    # locate the height of "From"
    y_coordinates = []
    addressee_zone_samples = []
    for sample in addresses.keys():
        height_From = None
        if sample.find('from') != -1 or sample.find('From') != -1:
            height_From = int(
                (addresses[sample][0][3] + addresses[sample][0][1]) / 2)
        else:
            y_coordinates.append(int(
                (addresses[sample][0][3] + addresses[sample][0][1]) / 2))
            addressee_zone_samples.append(sample)
    if height_From is None:
        # returns the first email address
        print('WARNING: "From" wasn\'t found')
        for sample in addressee_zone_samples:
            if sample.find('@') != -1:
                return sample
    # select the email address aligned with "From"
    i = np.argmin(np.array(y_coordinates) - height_From)
    while addressee_zone_samples[i].find('@') == -1:
        y_coordinates.pop(i)
        addressee_zone_samples.pop(i)
        i = np.argmin(np.array(y_coordinates) - height_From)
    return addressee_zone_samples[i]


def paragraph_detection(img: ImageType) -> list:
    '''
    Breaks down the text of an image into paragraphs

    Parameters
    ----------
    img : PIL.Image.Image
        Pillow image (the screenshot)
    result: list
        a list of str corresponding to each paragraph detected on the image
    '''
    text = pytesseract.image_to_string(img)
    lines = text.split('\n')
    paragraphs = []
    paragraph = ''
    for line in lines:
        if line == '':
            paragraphs.append(paragraph)
            paragraph = ''
        else:
            paragraph += line + "\n"
    return paragraphs
