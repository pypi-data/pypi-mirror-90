#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""


from typing import Optional, Tuple

from ..label import AttributeInfo, AttributeType, Catalog, CategoryInfo, LabelType
from ..utility import NameOrderedDict
from .pipeline import ErrorGenerator, PipelineForIterable
from .report import Error


class AttributeInfoError(Error):  # pylint: disable=too-few-public-methods
    """The base class of the AttributeInfo error

    :param name: the attribute name which has error
    """

    def __init__(self, name: str) -> None:
        self._name = name


ATTRIBUTE_INFO_PIPELINE: PipelineForIterable[
    AttributeInfo, AttributeInfoError
] = PipelineForIterable()


def check_catalog(
    catalog: Catalog,
) -> ErrorGenerator[Tuple[LabelType, AttributeInfoError]]:
    """the health check function for Catalog

    :param catalog: the Catalog object needs to be checked
    :return: a generator of `LabelType` and `AttributeInfoError`
    """
    for label_type, subcatalog in catalog.items():
        categories = getattr(subcatalog, "categories", None)
        attributes = getattr(subcatalog, "attributes", None)
        if attributes:
            attribute_info_pipeline = ATTRIBUTE_INFO_PIPELINE.copy()
            attribute_info_pipeline.register(CheckParentCategories(categories))
            for error in attribute_info_pipeline(attributes.values()):
                yield label_type, error


class InvalidTypeError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for invalid AttributeInfo 'type' field"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": "type" field is invalid'


@ATTRIBUTE_INFO_PIPELINE.register
def check_invalid_type(attribute_info: AttributeInfo) -> ErrorGenerator[InvalidTypeError]:
    """the health check function for invalid AttributeInfo 'type' field

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `InvalidTypeError`
    """
    if attribute_info.attribute_type is None:
        return

    if attribute_info.attribute_type == AttributeType.null:
        yield InvalidTypeError(attribute_info.name)
        return

    if not isinstance(attribute_info.attribute_type, list):
        return

    length = len(attribute_info.attribute_type)
    if length in (0, 1):
        yield InvalidTypeError(attribute_info.name)
        return

    if len(set(attribute_info.attribute_type)) != length:
        yield InvalidTypeError(attribute_info.name)


class InvalidEnumError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for invalid AttributeInfo 'enum' field"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": "enum" field is invalid'


@ATTRIBUTE_INFO_PIPELINE.register
def check_invalid_enum(attribute_info: AttributeInfo) -> ErrorGenerator[InvalidEnumError]:
    """the health check function for invalid AttributeInfo 'enum' field

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `InvalidEnumError`
    """
    if attribute_info.enum is None:
        return

    length = len(attribute_info.enum)
    if length in (0, 1):
        yield InvalidEnumError(attribute_info.name)
        return

    if len(set(attribute_info.enum)) != length:
        yield InvalidEnumError(attribute_info.name)


class NeitherTypeNorEnumError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for AttributeInfo which has neither 'enum' nor 'type' field"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Neither "type" nor "enum" field exists'


@ATTRIBUTE_INFO_PIPELINE.register
def check_neither_type_nor_enum(
    attribute_info: AttributeInfo,
) -> ErrorGenerator[NeitherTypeNorEnumError]:
    """the health check function for AttributeInfo which has neither 'enum' nor 'type' field

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `NeitherTypeNorEnumError`
    """
    if attribute_info.enum is None and attribute_info.attribute_type is None:
        yield NeitherTypeNorEnumError(attribute_info.name)


class RedundantTypeError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for AttributeInfo which has both 'enum' and 'type' field"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": "type" field is redundant when "enum" field exists'


@ATTRIBUTE_INFO_PIPELINE.register
def check_redundant_type(attribute_info: AttributeInfo) -> ErrorGenerator[RedundantTypeError]:
    """the health check function for AttributeInfo which has both 'enum' and 'type' field

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `RedundantTypeError`
    """
    if attribute_info.enum is not None and attribute_info.attribute_type is not None:
        yield RedundantTypeError(attribute_info.name)


class RangeNotSupportError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for AttributeInfo which has range for non number type"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Only "number" and "integer" type supports range'


@ATTRIBUTE_INFO_PIPELINE.register
def check_range_not_support(attribute_info: AttributeInfo) -> ErrorGenerator[RangeNotSupportError]:
    """the health check function for AttributeInfo which has range for non number type

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `RangeNotSupportError`
    """
    if attribute_info.maximum is None and attribute_info.minimum is None:
        return

    if isinstance(attribute_info.attribute_type, list):
        if AttributeType.number in attribute_info.attribute_type:
            return

        if AttributeType.integer in attribute_info.attribute_type:
            return

    elif attribute_info.attribute_type in (AttributeType.number, AttributeType.integer):
        return

    yield RangeNotSupportError(attribute_info.name)


class InvalidRangeError(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for AttributeInfo which has invalid range"""

    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Maximum is not larger than minimum'


@ATTRIBUTE_INFO_PIPELINE.register
def check_invalid_range(attribute_info: AttributeInfo) -> ErrorGenerator[InvalidRangeError]:
    """the health check function for AttributeInfo which has invalid range

    :param attribute_info: the AttributeInfo object needs to be checked
    :return: a generator of `InvalidRangeError`
    """
    if attribute_info.maximum is None or attribute_info.minimum is None:
        return

    if attribute_info.maximum > attribute_info.minimum:
        return

    yield InvalidRangeError(attribute_info.name)


class InvalidParentCategories(AttributeInfoError):  # pylint: disable=too-few-public-methods
    """the error class for AttributeInfo which has invalid parent categories,
    which means the category in parent_categories cannot be found in Subcatalog.categories

    :param name: the name of the incorrect attribute
    :param invalid_parent_category: the name of the incorrect parent_category
    """

    def __init__(self, name: str, invalid_parent_category: str) -> None:
        super().__init__(name)
        self._invalid_parent_category = invalid_parent_category

    def __str__(self) -> str:
        return (
            f'AttributeInfo "{self._name}":'
            f'parent category "{self._invalid_parent_category}" is invalid'
        )


class CheckParentCategories:  # pylint: disable=too-few-public-methods
    """the health check class for AttributeInfo which has invalid parent_categories

    :param categories: the dict of CategoryInfo which indicates all valid parent categories
    """

    def __init__(self, categories: Optional[NameOrderedDict[CategoryInfo]]) -> None:
        if not categories:
            categories = NameOrderedDict()
        self._categories = categories

    def __call__(self, attribute_info: AttributeInfo) -> ErrorGenerator[InvalidParentCategories]:
        """the health check function for AttributeInfo which has invalid parent_categories

        :param attribute_info: the AttributeInfo object needs to be checked
        :return: a generator of `InvalidRangeError`
        """
        for parent_category in attribute_info.parent_categories:
            if parent_category not in self._categories:
                yield InvalidParentCategories(attribute_info.name, parent_category)
