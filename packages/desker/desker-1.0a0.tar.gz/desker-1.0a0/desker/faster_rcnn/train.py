#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:12:19 2020

@author: jpd
"""
import argparse
import os
import time

import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from torchvision.models.detection.faster_rcnn import (FasterRCNN,
                                                      FastRCNNPredictor)

from desker.faster_rcnn.engine import (train_one_epoch,
                                       train_one_epoch_with_grad_accumulation)
from desker.faster_rcnn.screen_data import ScreenDataset, get_transform
from desker.faster_rcnn.utils import collate_fn


def get_FasterRCNN_model(num_classes: int) -> FasterRCNN:
    # load an instance segmentation model pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
        pretrained=True)

    # get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model


def train(
        annotations: str,
        epochs: int,
        batch_size: int,
        device: str,
        learning_rate: float = 0.005,
        momentum: float = 0.9,
        weight_decay: float = 0.0005,
        accumulation_steps=None) -> (FasterRCNN, ScreenDataset):

    writer = SummaryWriter(log_dir="./logs")
    # loss_tracker = []

    dataset = ScreenDataset(
        transforms=get_transform(train=True),
        json_file=annotations)
    num_labels = dataset.nb_classes()

    print(f"Training on files from '{dataset.root}' "
          f"({len(dataset)} images, {num_labels} classes)")

    data_loader = torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        collate_fn=collate_fn)

    # get the model using our helper function
    model = get_FasterRCNN_model(num_labels)
    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=learning_rate,
                                momentum=momentum, weight_decay=weight_decay)
    # and a learning rate scheduler which decreases the learning rate by
    # 10x every 5 epochs
    # lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
    #                                                step_size=5,
    #                                                gamma=0.1)

    # Training
    start_training = time.perf_counter()
    if accumulation_steps is None:
        for epoch in range(epochs):
            loss = train_one_epoch(
                model,
                optimizer,
                data_loader,
                device,
                epoch,
                print_freq=10)
            # update the learning rate
            # lr_scheduler.step()
            for key, value in loss.items():
                writer.add_scalar(f"{key}/train", value, epoch)
    else:
        for epoch in range(epochs):
            loss = train_one_epoch_with_grad_accumulation(
                model,
                optimizer,
                data_loader,
                device,
                epoch,
                print_freq=10,
                accumulation_steps=accumulation_steps)
            # update the learning rate
            # lr_scheduler.step()

    # P = pd.DataFrame(loss_tracker)
    print("\nTraining duration: {0}min {1}sec".format(
        int((time.perf_counter() - start_training) // 60),
        round((time.perf_counter() - start_training) % 60, 3)))

    writer.close()
    return model, dataset


if __name__ == "__main__":
    wd = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(
        prog="train.py",
        description="Fine-tune a pre-trained faster RCNN model with resnet 50 backbone")  # noqa: E501
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default='model_{0}.frcnn'.format(
            time.strftime(
                "%Hh%M",
                time.localtime())),
        help="name of the weight file generated after training")
    parser.add_argument(
        "-a",
        "--annotations",
        type=str,
        help="input json file containing annotations information",
    )
    parser.add_argument(
        "-c",
        "--classes",
        type=str,
        help="output json file giving the classes supported by the model",
        default=os.path.join(wd, "labels.json"),
    )
    parser.add_argument(
        "-e",
        "--epochs",
        type=int,
        default='5',
        help="number of epochs for training",
    )
    parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        default='2',
        help="batch size: number of images passed through the model \
            before gradient descent",
    )
    parser.add_argument(
        "-g",
        "--accumulation-steps",
        type=int,
        default=None,
        help="gradient accumulation parameter: number of backward passes \
            (calculation and accumulation of gradients after passing a batch) \
            before uptdating the model's parameters with: optimizer.step() \
            default = None",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        default="cuda",
        choices=['cpu', 'cuda'],
        help="Device to use for the model"
    )
    parser.add_argument(
        "-l",
        "--learning-rate",
        dest="learning_rate",
        type=float,
        default=5e-3,
        help="The learning rate")
    parser.add_argument(
        "-m",
        "--momentum",
        type=float,
        default=0.90,
        help="The momentum")
    parser.add_argument(
        "-w",
        "--weight-decay",
        dest="weight_decay",
        type=float,
        default=5e-4,
        help="The L2 penalization")
    args = parser.parse_args()

    device = torch.device(
        'cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(f"Device: {device}")

    if args.accumulation_steps is None:
        print("Training without gradient accumulation")
        model, dataset = train(
            annotations=args.annotations,
            epochs=args.epochs,
            batch_size=args.batch_size,
            device=args.device,
            learning_rate=args.learning_rate,
            momentum=args.momentum,
            weight_decay=args.weight_decay)
    else:
        print("\nTraining with gradient accumulation")
        model, dataset = train(
            annotations=args.annotations,
            epochs=args.epochs,
            batch_size=args.batch_size,
            device=args.device,
            learning_rate=args.learning_rate,
            momentum=args.momentum,
            weight_decay=args.weight_decay,
            accumulation_steps=args.accumulation_steps)

    # Model saving
    model.to('cpu')
    print(f"Saving model to {args.output}")
    torch.save(model.state_dict(), args.output)
    print(f"Saving classes to {args.classes}")
    dataset.save_labels(args.classes)
