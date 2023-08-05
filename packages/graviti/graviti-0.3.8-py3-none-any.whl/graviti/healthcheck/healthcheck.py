#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""


from typing import Union

from ..dataset import Dataset, FusionDataset
from .basic_check import check_basic
from .catalog_check import check_catalog
from .report import HealthReport


def healthcheck(dataset: Union[Dataset, FusionDataset]) -> HealthReport:
    """healthcheck for `Dataset` and `FusionDataset` object

    :param dataset: the `Dataset` or `FusionDataset` for healthchecking
    :return: the full result of the healthcheck which contains all errors found
    """
    report = HealthReport()

    with report.basic_reports as basic_reports:
        for basic_error in check_basic(dataset):
            basic_reports.append(basic_error)

    with report.subcatalog_reports as subcatalog_reports:
        for label_type, attribute_info_error in check_catalog(dataset.catalog):
            subcatalog_reports[label_type].append(attribute_info_error)

    return report
