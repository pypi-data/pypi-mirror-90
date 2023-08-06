#!/usr/bin/env python3

import argparse
import io
import json
import logging
from typing import List, Optional

from flask import Flask, Response, jsonify, request, send_file
from flask_restplus import Api, Resource, fields, inputs
from PIL import Image
from werkzeug.datastructures import FileStorage

import desker.faster_rcnn.predict as faster_rcnn
import desker.ocr.detect as ocr
import desker.settings as settings
from desker.login import cnn, knn
from desker.nlp.pipotron.bow import BagOfWords
from desker.nlp.pipotron.template import Template
from desker.utils import init_app_logger, init_request_logger

# create the app and configure from settings.py
app = Flask("Desker", instance_relative_config=True)
app.debug = False
app.config.from_object(settings)

# define custom loggers
app_logger = init_app_logger(app)
req_logger = init_request_logger(app)

# restplus API
api = Api(app,
          title="Desker",
          description="Desktop Elements Recognition (service app)")


@app.after_request
def log_request(response: Response) -> Response:
    """
    This function log requests after the server
    sends the response.
    It can access the 'request' object (and the
    'response too) and must forward the response.
    """
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/swagger'):
        return response

    line = f"\033[1m{request.method:7s}\033[0m {request.path}"
    if response.status_code != 200:
        line = f"\033[91;1m{request.method:7s}\033[0m "
        line += f"\033[91m{request.path}\033[0m"
    req_logger.info(line)
    return response


# Parsers =================================================================== #
# =========================================================================== #
# =========================================================================== #
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           help="A screenshot (image file)",
                           type=FileStorage, required=True)


# Models ==================================================================== #
# =========================================================================== #
# =========================================================================== #
faster_rcnn_output = api.model(
    name="Faster R-CNN output",
    model={
        'boxes': fields.List(fields.List(fields.Float), example=[
            [19.10693359375, 169.41688537597656,
             57.97800827026367, 223.6888427734375],
            [136.22616577148438, 297.3447570800781,
             191.30116271972656, 345.734130859375]
        ]),
        'labels': fields.List(fields.String,
                              example=["folder", "thunderbird"]),
        'scores': fields.List(fields.Float,
                              example=[0.9092492461204529,
                                       0.8558928966522217])},
)

wild = fields.Wildcard(fields.List(fields.List(fields.Integer)),
                       example=[[572, 531, 619, 546],
                                [791, 531, 838, 546]])
text_detection_output = api.model(
    name="Faster R-CNN output",
    model={"*": wild},
)


# OS Detection namespace ==================================================== #
# =========================================================================== #
# =========================================================================== #
os_detection = api.namespace('os_detection',
                             description='Detect OS from screenshots')

upload_parser_os = upload_parser.copy()
upload_parser_os.add_argument(
    'proba',
    location="args",
    required=False,
    help="Return the probability associated with every OS",
    type=inputs.boolean)


@os_detection.route(
    '/from_login',
    methods=['POST'],
    doc={
        "description": "Detect OS from login page"})
# @os_detection.doc(params={
#     'file': 'A PNG file (screenshot of login page)',
#     "proba": 'Return the probability associated with every OS'})
@os_detection.expect(upload_parser_os)
class OSDetection(Resource):
    def post(self):
        """Detect the OS from the login page
        """
        parameters = upload_parser_os.parse_args(request)
        req_logger.debug(f"{parameters}")
        img = parameters["file"]
        proba = parameters.get("proba", False)
        if proba:
            return jsonify(knn.predict_proba_from_image(Image.open(img)))
        return jsonify({"os": knn.predict_from_image(Image.open(img))})


@os_detection.route(
    '/is_login',
    methods=['POST'],
    doc={
        "description": "Detect if a screenshot is a login page"})
# @os_detection.doc(params={
#     'file': 'A PNG file (screenshot)',
#     "proba": 'Rather return the probability to be a login page'})
@os_detection.expect(upload_parser_os)
class LoginDetection(Resource):
    def post(self):
        """Detect whether an image looks like a login page
        """
        parameters = upload_parser_os.parse_args(request)
        req_logger.debug(f"{parameters}")
        img = Image.open(parameters["file"]).convert("RGB")
        proba = parameters.get("proba", False)
        if proba:
            p: float = cnn.login_page_probability(img)
            return {"proba": float(p)}
        login: bool = cnn.is_login_page(img)
        return {"is_login": bool(login)}


# Object Detection namespace (FasterRCNN) =================================== #
# =========================================================================== #
# =========================================================================== #
object_detection = api.namespace('object_detection',
                                 description='Detect desktop object from screenshot')  # noqa: E501
# object_detection.parser()
upload_parser_obj = upload_parser.copy()
upload_parser_obj.add_argument('filter',
                               location="form",
                               default=False,
                               required=False,
                               type=inputs.boolean)
upload_parser_obj.add_argument('threshold',
                               location="form",
                               required=False,
                               default=0.0,
                               type=float)


@object_detection.route(
    '/all',
    methods=['POST'],
    doc={"description": "Detect desktop objects from screenshot"})
@object_detection.expect(upload_parser_obj)
class ObjectDetection(Resource):
    def post(self):
        """Detect desktop elements (icons, folder, buttons etc.)
        """
        parameters = upload_parser_obj.parse_args()
        req_logger.debug(f"{parameters}")

        img = parameters["file"]
        filter_predictions = parameters.get("filter", False)
        threshold = parameters.get("threshold", 0.0)
        # To avoid: TypeError: Object of type ndarray is not JSON serializable
        # use .tolist() instead od .np()
        prediction = faster_rcnn.predict_elements(
            Image.open(img).convert("RGB"),
            filter_predictions=filter_predictions,
            threshold=threshold)

        return jsonify(prediction)


upload_parser_obj_single = upload_parser.copy()
upload_parser_obj_single.add_argument('label',
                                      location="form",
                                      required=True,
                                      type=str)


@object_detection.route(
    '/single',
    methods=['POST'],
    doc={"description": "Detect the given object only"})
@object_detection.expect(upload_parser_obj_single)
class ObjectDetectionSingle(Resource):
    def post(self):
        """Detect desktop elements (icons, folder, buttons etc.)
        """
        parameters = upload_parser_obj_single.parse_args()
        req_logger.debug(f"{parameters}")

        img = parameters["file"]
        label = parameters["label"]

        prediction = faster_rcnn.predict_single(
            Image.open(img).convert("RGB"),
            label=label)

        return jsonify(prediction)


upload_parser_demo = upload_parser.copy()
upload_parser_demo.add_argument('threshold',
                                location="args",
                                help="Minimum score of a prediction",
                                required=False,
                                default=0.0,
                                type=float)


@object_detection.route(
    '/all/demo',
    methods=['POST'],
    doc={
        "description":
        "Detect desktop objects from screenshot "
        "but return the input image annotated"})
@object_detection.expect(upload_parser_demo)
class ObjectDetectionDemo(Resource):
    def post(self):
        """
        Detect desktop elements (icons, folder, buttons...) and
        return the annotated image
        """
        parameters = upload_parser_demo.parse_args(request)
        req_logger.debug(f"{parameters}")
        # open the image to get its type
        img = Image.open(parameters["file"])
        img_type = img.format.lower()
        th = parameters.get("threshold", 0.0)

        # get the annotations
        annotated_image = faster_rcnn.predict_elements_demo(
            img.convert("RGB"), model=None, threshold=th)
        # put the image into a io buffer (recommended way)
        buffer = io.BytesIO()
        annotated_image.save(buffer, format=img_type)
        buffer.seek(0)
        # returns the image
        return send_file(
            buffer,
            mimetype=f'image/{img_type}',
            cache_timeout=10)


# Text Detection namespace (Tesseract) ====================================== #
# =========================================================================== #
# =========================================================================== #
text_detection = api.namespace(
    'text_detection',
    description='Detect text boxes and recognize characters from screenshot')


@text_detection.route(
    '/all',
    methods=['POST'],
    doc={"description": "Detect text boxes and recognize "
         "characters from screenshot"})
@text_detection.expect(upload_parser)
class TextDetection(Resource):
    def post(self):
        """
        Get all the text inside the image

        Returns
        -------
        It returns a dict those keys are words and
        values are boxes where the word is found
        """
        parameters = upload_parser.parse_args(request)
        req_logger.debug(f"{parameters}")
        img = parameters["file"]
        prediction = ocr.get_boxes(Image.open(img))
        return jsonify(prediction)


text_under_box_parser = upload_parser.copy()
text_under_box_parser.add_argument(
    "boxes",
    type=str,
    action="append",
    location="form",
    help='A list of boxes (4-values tuple [xmin, ymin, xmax, ymax])',
    required=True)


@text_detection.route(
    '/under_box',
    methods=['POST'],
    doc={"description": "Detect text below given boxes"})
@text_detection.expect(text_under_box_parser)
class TextUnderBoxDetection(Resource):
    def post(self):
        """
        Detect text below given boxes
        """
        parameters = text_under_box_parser.parse_args(request)
        req_logger.debug(f"{parameters}")
        img = parameters["file"]
        boxes = json.loads(parameters["boxes"][0])
        prediction = ocr.get_text_under_boxes(
            Image.open(img), boxes)
        return jsonify(prediction)


upload_parser_links = upload_parser.copy()
upload_parser_links.add_argument(
    "result",
    default="centers",
    location="form",
    type=str,
    choices=["centers", "boxes"],
    help="Type of the returned result (centers or boxes)",
)
upload_parser_links.add_argument(
    "link_colors",
    action="split",
    location="form",
    default=["#0645AD"],
    help="List of considered link colors")


@text_detection.route(
    '/links',
    methods=['POST'],
    doc={"description": "Detect links"})
@text_detection.expect(upload_parser_links)
class LinkDetection(Resource):
    def post(self):
        """
        Detect links in text areas (like on a Wikipédia page)
        """
        parameters = upload_parser_links.parse_args(request)
        req_logger.debug(f"{parameters}")
        img = parameters["file"]
        link_colors = parameters["link_colors"]
        # print(link_colors, type(link_colors))
        result = parameters["result"]
        req_logger.debug(f"[parameters] result: {result} ({type(result)}) "
                         f"link_colors: {link_colors} ({type(link_colors)})")
        prediction = ocr.get_links(
            Image.open(img).convert("RGB"),
            result=result,
            link_colors=link_colors)
        return jsonify(prediction)


upload_parser_blocks = upload_parser.copy()
upload_parser_blocks.add_argument(
    "min_occupation",
    type=float,
    default=1e-5,
    location="form",
    help="Minimum surface of the windows in comparison to the whole image",
)
upload_parser_blocks.add_argument(
    "max_occupation",
    type=float,
    default=0.95,
    location="form",
    help="Maximum surface of the windows in comparison to the whole image",
)
upload_parser_blocks.add_argument(
    "min_aspect",
    type=float,
    default=1 / 15,
    location="form",
    help="Minimum ratio width/height. It means that w/h > min_aspect",
)
upload_parser_blocks.add_argument(
    "max_aspect",
    type=float,
    default=15.,
    location="form",
    help="Maximum ratio width/height. It means that w/h < max_aspect",
)


@text_detection.route(
    '/blocks',
    methods=['POST'],
    doc={"description": "Detect blocks"})
@text_detection.expect(upload_parser_blocks)
class BlockDetection(Resource):
    def post(self):
        """
        Find "relevant blocks" within an image, like paragraphs,
        side bars, banners etc.
        It returns a list of masks (matrices)
        corresponding to the detected areas.
        """
        parameters = upload_parser_blocks.parse_args(request)
        req_logger.debug(f"{parameters}")

        img = parameters["file"]

        _, masks = ocr.find_blocks(
            Image.open(img).convert("RGB"),
            min_occupation=parameters["min_occupation"],
            max_occupation=parameters["max_occupation"],
            min_aspect=parameters["min_aspect"],
            max_aspect=parameters["max_aspect"])

        return jsonify([m.tolist() for m in masks])


# Pipotron namespace ==================================================== #
# =========================================================================== #
# =========================================================================== #
pipotron = api.namespace('pipotron',
                         description='Generate pseudo-random text')

pipotron_mail_parser = api.parser()
pipotron_mail_parser.add_argument(
    "mail_to",
    default="Charles-Edouard",
    type=str,
    help="Mail destination name"
)


@pipotron.route(
    '/generate_mail',
    methods=['POST'],
    doc={"description": "Generate pseudo-random mail"})
@pipotron.doc(params={
    'mail_to': 'Mail destination name',
})
@pipotron.expect(pipotron_mail_parser)
class PipotronMail(Resource):
    def post(self):
        """
        Generate pseudo-random mail
        """
        parameters = pipotron_mail_parser.parse_args(request)
        req_logger.debug(f"{parameters}")
        mail_to = parameters["mail_to"]
        req_logger.debug(f"[parameters] mail_to: {mail_to} ({type(mail_to)}) ")

        # Generate mail content
        t = Template("laboralphy.yml")
        t.render()
        mail = Template("email.yml")
        BagOfWords().add("destinataire", mail_to)

        mail_content = mail.render()

        return jsonify(mail_content)


def start(cli_args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        "desker", description="Desktop Elements Recognition")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5000,
        help="Port to bind")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Listening address")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Debug mode")

    arguments = parser.parse_args(cli_args)
    if arguments.debug:
        app_logger.root.setLevel(logging.DEBUG)
    else:
        app_logger.root.setLevel(logging.INFO)

    # init the models
    try:
        app_logger.info("Importing vm detection model")
        knn.import_model()

        app_logger.info("Importing login detection model")
        cnn.load_model()

        app_logger.info("Importing desktop element detection model")
        faster_rcnn.load_model()
    except FileNotFoundError as err:
        app_logger.error(f"Fail to load some models: {err}")

    app_logger.info(
        f"Ready to listen on http://{arguments.host}:{arguments.port}")
    app.run(debug=False, host=arguments.host, port=arguments.port)


if __name__ == '__main__':
    start()
