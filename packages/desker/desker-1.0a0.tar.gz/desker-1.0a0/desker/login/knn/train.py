#!/usr/bin/env python3

import argparse
import logging
import os
import sys

import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier as KNN

from desker.login.knn.predict import load_data


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        if record.levelno == logging.INFO:
            record.levelname = '\033[32m[{:>8s}]\033[0m'.format(
                record.levelname)
        elif record.levelno == logging.WARNING:
            record.levelname = '\033[33m[{:>8s}]\033[0m'.format(
                record.levelname)
        elif record.levelno == logging.CRITICAL:
            record.levelname = '\033[31m[{:>8s}]\033[0m'.format(
                record.levelname)
        return super().format(record)


def learn(csv_file: str, img_dir: str) -> KNN:
    """
    Learn a basic k nearest neighbor classifier

    Parameters
    ----------

    csv_file : str
        Path to the csv file storing the labels
    img_dir : str
        Directory which contains the images
    """
    P = pd.read_csv(csv_file)
    data = load_data(P, img_dir)
    knn = KNN(n_neighbors=1)
    # it must be sorted to ensure that values
    # are in the right order
    keys = [c for c in sorted(data.columns) if c not in ["path", "label"]]
    X = data[keys]
    y = data['label']
    knn.fit(X, y)
    return knn


def save(model: KNN, path: str) -> str:
    """
    Save a model to the given file
    """
    return joblib.dump(model, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="train.py",
        description="Train a mini OS classifier from login page"
    )

    parser.add_argument("img_dir",
                        type=str,
                        help="Path to the login screenshots")
    parser.add_argument("-o", "--output",
                        help="File where the model will be saved")
    parser.add_argument("-l", "--labels",
                        type=str, help="csv file gathering the labels")
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(ColoredFormatter('%(levelname)s %(message)s'))
    logger.addHandler(console)

    img_dir = args.img_dir
    if not os.path.exists(img_dir):
        logging.fatal("The directory {:s} does not exist".format(img_dir))
        sys.exit(1)

    csv = args.labels
    if csv is None:
        csv = os.path.join(img_dir, "labels.csv")
        logging.warning("Label file not given, using {:s}".format(csv))

    if not os.path.exists(csv):
        logging.fatal("The file {:s} does not exist".format(csv))
        sys.exit(2)

    logging.info("Training model from {:s}".format(img_dir))
    model = learn(csv_file=csv, img_dir=img_dir)

    output = args.output
    if output is None:
        output = os.path.join(img_dir, "model.knn")
        logging.warning("Output file not given, using {:s}".format(output))

    logging.info("Saving model to {:s}".format(output))
    save(model, output)
