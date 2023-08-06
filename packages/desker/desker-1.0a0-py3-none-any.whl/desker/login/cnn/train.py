#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import tempfile
from math import sqrt
from typing import Callable, List, Optional

import coloredlogs
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
from PIL import Image
from PIL.Image import Image as ImageType

__default_device__ = 'cuda' if torch.cuda.is_available() else 'cpu'


class Crop(object):
    """Returns an image without left/right black borders"""

    # 3 channels
    def __call__(self, img: ImageType) -> ImageType:
        M = np.asarray(img)
        Z = (M[:, :, 0] == 0) & (M[:, :, 1] == 0) & (M[:, :, 2] == 0)
        cols = Z.all(axis=0)
        rows = Z.all(axis=1)
        return Image.fromarray(M[:, ~cols, :][~rows, :, :])

    # 1 channel
    # def __call__(self, img : Image) -> Image:
    #     M = np.asarray(img)
    #     print(M.shape)
    #     Z = (M[:, :] == 0)
    #     cols = Z.all(axis=0)
    #     rows = Z.all(axis=1)
    #     return Image.fromarray(M[:, ~cols][~rows, :])


class Net(nn.Module):
    def __init__(self, img_size: int = 64):
        super(Net, self).__init__()
        self.img_size = img_size
        self.m = self.img_size // 4 - 3
        self.conv1 = nn.Conv2d(3, 6, 5)
        # self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * self.m * self.m, (self.m // 4)**2)
        self.fc2 = nn.Linear((self.m // 4)**2, (self.m // 6)**2)
        self.fc3 = nn.Linear((self.m // 6)**2, 2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool(F.relu(x))
        x = self.conv2(x)
        x = self.pool(F.relu(x))
        # flatten
        x = x.view(-1, 16 * self.m * self.m)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def get_transform(self) -> Callable:
        return transforms.Compose([
            Crop(),
            transforms.Resize(size=(self.img_size, self.img_size)),
            transforms.ToTensor()])

    def train(self,
              dataloader: torch.utils.data.DataLoader,
              testloader: Optional[torch.utils.data.DataLoader] = None,
              keep_best_test_model: bool = True,
              criterion: nn.modules.loss._Loss = nn.CrossEntropyLoss(),
              lr: float = 1e-4,
              momentum: float = 0.9,
              nb_epochs: int = 30) -> None:

        # test
        best_model = self.state_dict().copy()
        best_test_score = -1

        optimizer = optim.SGD(self.parameters(), lr=lr, momentum=momentum)
        for epoch in range(nb_epochs):  # loop over the dataset multiple times

            # Training ====================================================== #
            # =============================================================== #
            running_loss = 0.0
            running_corrects = 0
            for inputs, labels in dataloader:
                labels = labels.flatten()
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.__call__(inputs)
                _, preds = torch.max(outputs, 1)
                # print(outputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            print(
                f"[EPOCH {epoch+1}/{nb_epochs}]\t"
                f"loss: {running_loss:.6f}\t"
                f"correct: {running_corrects}/"
                f"{dataloader.sampler.num_samples}",
                end='\t' if testloader else '\n')
            # Testing ======================================================= #
            # =============================================================== #
            if testloader:
                running_loss = 0.0
                running_corrects = 0
                for inputs, labels in testloader:
                    labels = labels.flatten()

                    # forward
                    outputs = self.__call__(inputs)
                    _, preds = torch.max(outputs, 1)

                    loss = criterion(outputs, labels)

                    # print statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                print(
                    f"| TEST\tloss: {running_loss:.6f}\t"
                    f"correct: {running_corrects}/"
                    f"{testloader.sampler.num_samples}\t")
                if running_corrects >= best_test_score:
                    print("-> Keeping this model")
                    best_model = self.state_dict().copy()
                    best_test_score = running_corrects

        # keeping best model
        if keep_best_test_model:
            self.load_state_dict(best_model)

    def basic_test(self, folder: str) -> (int, int):
        """
        Parameters
        ----------
        folder : str
            path to screenshots

        Returns
        -------
        int
            number_of_login_images_detected
        int
            number_of_images
        """
        s = 0
        for f in os.listdir(folder):
            img = Image.open(os.path.join(folder, f)).convert("RGB")
            s += self.predict_single_image(img)
        return s, len(os.listdir(folder))

    def save(self, path: str) -> None:
        torch.save(self.state_dict(), path)

    @staticmethod
    def from_model(path: str, device: str = __default_device__) -> 'Net':
        """
        Return a Net instance based on a saved model

        Parameters
        ----------
        path : str
            path to the model
        """
        state_dict = torch.load(path, map_location=torch.device(device))
        _, p = state_dict["fc1.weight"].shape
        # obscur calculus (see the __init__ function)
        img_size = int((sqrt(p // 16) + 3) * 4)
        net = Net(img_size)
        net.load_state_dict(state_dict)
        return net

    def load(self, path: str) -> None:
        self.load_state_dict(torch.load(path))

    def get_device(self) -> str:
        """
        Returns the device the model is stored on
        'cpu' or 'cuda'
        """
        if next(self.parameters()).is_cuda:
            return 'cuda'
        return 'cpu'

    def raw_score_single_image(self, img: ImageType) -> np.ndarray:
        tr = self.get_transform()
        data = tr(img).to(self.get_device())
        if data.ndim == 3:
            data = data[None, :, :, :]
        output = self.__call__(data)
        return output[0].detach().cpu().numpy()

    def predict_single_image(
            self,
            img: ImageType) -> int:
        output = self.raw_score_single_image(img)
        return np.argmax(output)


class LoginDataset(object):
    __extensions__ = ['png', 'jpg', 'jpeg', 'bmp']

    def __init__(self,
                 login_root: str,
                 notlogin_root: str,
                 transforms: Callable,
                 detect: bool = False,
                 device: str = __default_device__):
        """
        Parameters
        ----------

        login_root : str
            Path to directory which contains the login images
        notlogin_root : str
            Path to directory which contains the no-login images
        transforms : Callable
            Function to transform the PIL images
        detect : bool
            if True, does not send labels
        device : str
            Device to store the images ('cuda' or 'cpu')
        """
        self.login_root = os.path.abspath(login_root)
        self.notlogin_root = os.path.abspath(notlogin_root)
        self.detect = detect
        self.transforms = transforms
        self.device = device
        # login images
        self.login_imgs = self.__get_images(login_root)
        # other desktop images
        self.notlogin_imgs = self.__get_images(notlogin_root)

    def __get_images(self, path: str) -> List[str]:
        imgs = []
        for f in sorted(os.listdir(path)):
            for ext in self.__extensions__:
                if f.lower().endswith(ext):
                    imgs.append(os.path.join(path, f))
        return imgs

    def __getitem__(self, idx: int):
        lli = len(self.login_imgs)
        if idx < lli:
            img_path = self.login_imgs[idx]
            label = 1
        else:
            img_path = self.notlogin_imgs[idx - lli]
            label = 0

        raw_img = Image.open(img_path).convert("RGB")
        img = self.transforms(raw_img).to(self.device)
        if self.detect:
            # return directly without labels
            return img, None
        return img, torch.tensor([label], dtype=torch.long, device=self.device)

    def __len__(self) -> int:
        return len(self.login_imgs) + len(self.notlogin_imgs)


def main(cli_args: List[str]):
    parser = argparse.ArgumentParser(
        prog="train.py",
        description="Train a login page detector"
    )

    parser.add_argument("login_img_dir",
                        type=str,
                        help="Path to the login screenshots")
    parser.add_argument("notlogin_img_dir",
                        type=str,
                        help="Path to the no-login screenshots")
    parser.add_argument("-o", "--output", type=str,
                        help="File where the model will be saved")
    parser.add_argument("-d", "--device", type=str, choices=["cpu", "cuda"],
                        help="device to use",
                        default=__default_device__)
    parser.add_argument("-f", "--from-model", dest="from_model", type=str,
                        help="start from a given model")
    parser.add_argument("-s", "--size", type=int, default=256,
                        help="Input image size for the model (square image)")
    parser.add_argument(
        "-t",
        "--train-ratio",
        dest="train_ratio",
        type=float,
        default=0.90,
        help="Ratio of input images to train the CNN (other are for test)")
    parser.add_argument(
        "-b",
        "--batch-size",
        dest="batch_size",
        type=int,
        default=5,
        help="Number of images taken at every optimization step")
    parser.add_argument(
        "-e",
        "--epoch",
        type=int,
        default=20,
        help="Number of epochs")
    parser.add_argument(
        "-l",
        "--learning-rate",
        dest="learning_rate",
        type=float,
        default=1e-3,
        help="The learning rate")
    parser.add_argument(
        "-m",
        "--momentum",
        type=float,
        default=0.90,
        help="The momentum")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Erase the output file if it already exists")
    args = parser.parse_args(args=cli_args)

    # Create a logger object.
    logger = logging.getLogger()

    # By default the install() function installs a handler on the root logger,
    # this means that log messages from your code and log messages from the
    # libraries that you use will all show up on the terminal.
    coloredlogs.install(level='INFO', fmt='%(levelname)s %(message)s')

    # check device
    if args.device == "cuda" and __default_device__ != "cuda":
        raise OSError("The device 'cuda' seems not available")

    # Model creation
    if args.from_model:
        logger.info(f"Importing network from {args.from_model}")
        net = Net.from_model(args.from_model).to(args.device)
    else:
        logger.info(f"Creating model (image size: {args.size})")
        net = Net(img_size=args.size).to(args.device)
    logger.info(f"Model is put to {args.device}")

    # Dataset
    logger.info(f"Creating dataset from {args.login_img_dir} "
                f"and {args.notlogin_img_dir}")
    dataset = LoginDataset(
        login_root=args.login_img_dir,
        notlogin_root=args.notlogin_img_dir,
        transforms=net.get_transform(),
        device=args.device)

    train_size = int(args.train_ratio * len(dataset))
    test_size = len(dataset) - train_size

    train, test = torch.utils.data.random_split(dataset,
                                                [train_size, test_size])

    dataloader = torch.utils.data.DataLoader(train, batch_size=args.batch_size,
                                             shuffle=True, num_workers=0)

    testloader = torch.utils.data.DataLoader(test, batch_size=10,
                                             shuffle=True, num_workers=0)

    # preparing output
    if args.output:
        directory = os.path.dirname(args.output)
        if not os.path.exists(directory):
            raise OSError(f"The base directory {directory} does not exist")
        if os.path.exists(args.output) and not args.force:
            raise OSError(f"The file {args.output} already "
                          f"exists (use --force to ignore)")
        output = args.output
    else:
        output = tempfile.mktemp(suffix=".cnn")

    logger.info(f"Model will be saved to {output}")

    logger.info("Start training...")
    # train
    net.train(
        dataloader,
        testloader=testloader if len(testloader) > 0 else None,
        nb_epochs=args.epoch,
        lr=args.learning_rate,
        momentum=args.momentum)
    logger.info("Training is finished")
    logger.info(f"Saving model to {output}")
    net.save(output)


if __name__ == "__main__":
    args = list(sys.argv[1:])
    main(args)
