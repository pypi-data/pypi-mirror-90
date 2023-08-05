#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""OpenDataset dataloader collections."""

from .AnimalsWithAttributes2 import AnimalsWithAttributes2
from .CarConnection import CarConnection
from .CoinImage import CoinImage
from .DownsampledImagenet import DownsampledImagenet
from .Elpv import Elpv
from .Flower import Flower17, Flower102
from .FSDD import FSDD
from .HeadPoseImage import HeadPoseImage
from .ImageEmotion import ImageEmotionAbstract, ImageEmotionArtphoto
from .JHU_CROWD import JHU_CROWD
from .KenyanFood import KenyanFoodOrNonfood, KenyanFoodType
from .KylbergTexture import KylbergTexture
from .LISATrafficLight import LISATrafficLight
from .NeolixOD import NeolixOD
from .Newsgroups20 import Newsgroups20
from .THUCNews import THUCNews

__all__ = [
    "AnimalsWithAttributes2",
    "CarConnection",
    "CoinImage",
    "DownsampledImagenet",
    "Elpv",
    "Flower17",
    "Flower102",
    "ImageEmotionAbstract",
    "ImageEmotionArtphoto",
    "KenyanFoodOrNonfood",
    "KenyanFoodType",
    "KylbergTexture",
    "LISATrafficLight",
    "NeolixOD",
    "Newsgroups20",
    "FSDD",
    "JHU_CROWD",
    "HeadPoseImage",
    "THUCNews",
]
