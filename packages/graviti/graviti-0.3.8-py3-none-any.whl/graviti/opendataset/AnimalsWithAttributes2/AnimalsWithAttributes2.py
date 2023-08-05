#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define the Animals with attributes 2 Dataloader"""

import os

from ...dataset import Data, Dataset
from ...label import Classification
from .._utility import glob

DATASET_NAME = "AnimalsWithAttributes2"


def AnimalsWithAttributes2(path: str) -> Dataset:
    """
    Load the Animals with attributes 2 to TensorBay
    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        classes.txt
        predicates.txt
        predicate-matrix-binary.txt
        JPEGImages/
            <classname>/
                <imagename>.jpg
                ...
            ...

    :return: a loaded dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog.json"))
    segment = dataset.create_segment()

    with open(os.path.join(root_path, "classes.txt")) as fp:
        class_names = [line[:-1].split("\t", 1)[-1] for line in fp]

    with open(os.path.join(root_path, "predicates.txt")) as fp:
        attribute_keys = [line[:-1].split("\t", 1)[-1] for line in fp]

    with open(os.path.join(root_path, "predicate-matrix-binary.txt")) as fp:
        attribute_values_list = [line[:-1].split(" ") for line in fp]

    attribute_mapping = {}
    for class_name, values in zip(class_names, attribute_values_list):
        attribute_mapping[class_name] = Classification(
            category=class_name,
            attributes=dict(zip(attribute_keys, (bool(int(value)) for value in values))),
        )

    for class_name in sorted(os.listdir(os.path.join(root_path, "JPEGImages"))):
        image_paths = glob(os.path.join(root_path, "JPEGImages", class_name, "*.jpg"))
        label = attribute_mapping[class_name]
        for image_path in image_paths:
            data = Data(image_path)
            data.append_label(label)
            segment.append(data)

    return dataset
