import math
import sys

import numpy as np
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from torchvision.models.detection.faster_rcnn import FasterRCNN

import desker.faster_rcnn.utils as utils


def train_one_epoch(
        model: FasterRCNN,
        optimizer: Optimizer,
        data_loader: DataLoader,
        device: str,
        epoch: int,
        print_freq: int):
    """
    Perform one epoch optimization
    """
    model.train()
    metric_logger = utils.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr', utils.SmoothedValue(window_size=1,
                                                      fmt='{value:.6f}'))
    header = 'Epoch: [{}]'.format(epoch)

    lr_scheduler = None

    # loss_track = []

    # if epoch == 0:
    #     warmup_factor = 1. / 1000
    #     warmup_iters = min(1000, len(data_loader) - 1)

    #     lr_scheduler = utils.warmup_lr_scheduler(optimizer,
    #                                              warmup_iters,
    #                                              warmup_factor)

    epoch_logs = {}
    for images, targets in metric_logger.log_every(data_loader,
                                                   print_freq,
                                                   header):
        images = list(image.to(device) for image in images)

        # print("EPOCH_TARGET=", targets)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        next_loop = sum(map(lambda t: len(t["boxes"]) == 0, targets)) > 0
        if next_loop:
            print(next_loop)
            continue

        # forward
        loss_dict = model(images, targets)
        # logs = dict((k, float(t.cpu())) for k, t in loss_dict.items())
        # print(f"Loss dict: {logs}", flush=True)
        losses = sum(loss for loss in loss_dict.values())

        # reduce losses over all GPUs for logging purposes
        loss_dict_reduced = utils.reduce_dict(loss_dict, average=False)

        # overall loss among batch
        losses_reduced = sum(loss for loss in loss_dict_reduced.values())
        loss_value = losses_reduced.item()

        if not math.isfinite(loss_value):
            print("Loss is {}, stopping training".format(loss_value))
            sys.exit(1)

        # add loss to the global logs
        total = 0.
        for k in loss_dict_reduced:
            ll = float(loss_dict_reduced[k].cpu())
            epoch_logs[k] = epoch_logs.get(k, 0.) + ll
            total += ll
        epoch_logs['total'] = epoch_logs.get('total', 0.) + total

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        if lr_scheduler is not None:
            lr_scheduler.step()

        metric_logger.update(loss=losses_reduced, **loss_dict_reduced)
        metric_logger.update(lr=optimizer.param_groups[0]["lr"])
    return epoch_logs


def train_one_epoch_with_grad_accumulation(
        model,
        optimizer,
        data_loader,
        device,
        epoch,
        print_freq,
        accumulation_steps=1):
    model.train()
    metric_logger = utils.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr',
                            utils.SmoothedValue(window_size=1,
                                                fmt='{value:.6f}'))
    header = 'Epoch: [{}]'.format(epoch)

    lr_scheduler = None

    loss_track = []

    if epoch == 0:
        warmup_factor = 1. / 1000
        warmup_iters = min(1000, len(data_loader) - 1)

        lr_scheduler = utils.warmup_lr_scheduler(optimizer,
                                                 warmup_iters,
                                                 warmup_factor)

    step = 0
    for images, targets in metric_logger.log_every(data_loader,
                                                   print_freq,
                                                   header):
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        # forward
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values()) / accumulation_steps

        # reduce losses over all GPUs for logging purposes
        loss_dict_reduced = utils.reduce_dict(loss_dict)
        losses_reduced = sum(loss for loss in loss_dict_reduced.values())

        loss_value = losses_reduced.item()
        loss_track.append(loss_value)

        if not math.isfinite(loss_value):
            print("Loss is {}, stopping training".format(loss_value))
            print(loss_dict_reduced)
            sys.exit(1)

        if step % accumulation_steps == 0:
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
            print("parameters updated at step: {0}".format(step))
            if lr_scheduler is not None:
                lr_scheduler.step()

            metric_logger.update(loss=losses_reduced, **loss_dict_reduced)
            metric_logger.update(lr=optimizer.param_groups[0]["lr"])
        else:
            losses.backward()
            if lr_scheduler is not None:
                lr_scheduler.step()
            metric_logger.update(loss=losses_reduced, **loss_dict_reduced)

        step += 1
    return np.array(loss_track)


def _get_iou_types(model):
    return ["bbox"]
