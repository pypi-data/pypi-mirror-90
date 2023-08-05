#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetBase, Dataset and FusionDataset."""

import json
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, TypeVar, Union, overload

from typing_extensions import Literal

from ..label import AudioSubcatalog, Catalog, KeypointsSubcatalog, LabelType, Subcatalog
from ..label.catalog import Subcatalogs
from ..utility import NameClass, NameSortedList, ReprType
from .segment import FusionSegment, Segment

T = TypeVar("T", FusionSegment, Segment)  # pylint: disable=invalid-name


class _DataType(Enum):
    """this class defines the type of the data."""

    IMAGE = 0
    POINT_CLOUD = 1
    AUDIO = 2
    TEXT = 3
    OTHERS = 255


class DataType(Enum):
    """this class defines the type of the data."""

    IMAGE = "Image"
    POINT_CLOUD = "Point Cloud"
    AUDIO = "Audio"
    TEXT = "Text"
    OTHERS = "Others"


class DatasetBase(NameClass, Sequence[T]):
    """This class defines the concept of DatasetBase,
    which represents a whole dataset contains several segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    """

    _repr_type = ReprType.SEQUENCE

    def __init__(self, name: str, is_continuous: bool = False) -> None:
        super().__init__(name)
        self._segments: NameSortedList[T] = NameSortedList()
        self._catalog: Catalog = Catalog()
        self._is_continuous = is_continuous

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Sequence[T], T]:
        return self._segments.__getitem__(index)

    def __len__(self) -> int:
        return self._segments.__len__()

    @property
    def is_continuous(self) -> bool:
        """Check whether the data in dataset is continuous

        :return: Return `True` if the data is continuous, otherwise return `False`
        """
        return self._is_continuous

    @property
    def catalog(self) -> Catalog:
        """Return catalog

        :return: catalog
        """
        return self._catalog

    def load_catalog(self, loads: Union[Dict[str, Dict[str, Any]], str]) -> None:
        """Load catalog from json object.

        :param loads: Catalog dict or the name of the file which contains the Catalog dict
        """
        if isinstance(loads, str):
            with open(loads) as fp:
                catalog_dict = json.load(fp)
        else:
            catalog_dict = loads

        self._catalog = Catalog(loads=catalog_dict)

    @overload
    def create_subcatalog(
        self,
        label_type: Literal[
            LabelType.CLASSIFICATION,
            LabelType.BOX2D,
            LabelType.BOX3D,
            LabelType.POLYGON2D,
            LabelType.POLYLINE2D,
        ],
    ) -> Subcatalog:
        ...

    @overload
    def create_subcatalog(self, label_type: Literal[LabelType.KEYPOINTS2D]) -> KeypointsSubcatalog:
        ...

    @overload
    def create_subcatalog(self, label_type: Literal[LabelType.SENTENCE]) -> AudioSubcatalog:
        ...

    @overload
    def create_subcatalog(self, label_type: LabelType) -> Subcatalogs:
        ...

    def create_subcatalog(self, label_type: LabelType) -> Subcatalogs:
        """Create a new subcatalog with given label type and add it to catalog.

        :param label_type: the label type of the subcatalog to create

        :return: the created subcatalog
        """

        return self._catalog.create_subcatalog(label_type)

    @overload
    def get_subcatalog(
        self,
        label_type: Literal[
            LabelType.CLASSIFICATION,
            LabelType.BOX2D,
            LabelType.BOX3D,
            LabelType.POLYGON2D,
            LabelType.POLYLINE2D,
        ],
    ) -> Subcatalog:
        ...

    @overload
    def get_subcatalog(self, label_type: Literal[LabelType.KEYPOINTS2D]) -> KeypointsSubcatalog:
        ...

    @overload
    def get_subcatalog(self, label_type: Literal[LabelType.SENTENCE]) -> AudioSubcatalog:
        ...

    @overload
    def get_subcatalog(self, label_type: LabelType) -> Subcatalogs:
        ...

    def get_subcatalog(self, label_type: LabelType) -> Subcatalogs:
        """return the subcatalog corresponding to given LabeleType.

        :param label_type: a instance of LabelType
        :return: a subcatalog
        """

        return self._catalog[label_type]

    def get_label_types(self) -> Set[LabelType]:
        """return a set contains all label types.

        :return: a set of all label types
        """

        return set(self._catalog.keys())

    def get_segment_by_name(self, name: str) -> T:
        """return the segment corresponding to given name.

        :param name: name of the segment
        :return: the segment which matches the input name
        """

        return self._segments.get_from_name(name)

    def add_segment(self, segment: T) -> None:
        """add segment to segment list.

        :param segment: a segment to be added
        """

        self._segments.add(segment)


class Dataset(DatasetBase[Segment]):
    """This class defines the concept of dataset,
    which contains a list of segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    :param data_type: Type of the data
    """

    def __init__(
        self, name: str, is_continuous: bool = False, data_type: Optional[DataType] = None
    ) -> None:
        super().__init__(name, is_continuous)
        self._data_type = data_type

    @property
    def data_type(self) -> Optional[DataType]:
        """Type of the data

        :return: Return type of the data
        """
        return self._data_type

    def create_segment(self, segment_name: str = "") -> Segment:
        """create a segment with the given name.

        :param segment_name: The name of the created segment
        :return: The created segment
        """
        segment = Segment(segment_name)
        self._segments.add(segment)
        return segment


class FusionDataset(DatasetBase[FusionSegment]):
    """This class defines the concept of multi-sensor dataset,
    which contains a list of multi-sensor segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    :param data_type: Type of the data
    """

    def __init__(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Union[Iterable[DataType], DataType, None] = None,
    ) -> None:
        super().__init__(name, is_continuous)
        self._data_type: List[DataType]
        if not isinstance(data_type, Iterable):  # pylint: disable=W1116
            self._data_type = [data_type] if data_type else []
        else:
            self._data_type = list(data_type)

    @property
    def data_type(self) -> List[DataType]:
        """Type of the data

        :return: Return type of the data
        """
        return self._data_type

    def create_segment(self, segment_name: str = "") -> FusionSegment:
        """create a fusion segment with the given name.

        :param segment_name: The name of the created fusion segment
        :return: The created fusion segment
        """
        segment = FusionSegment(segment_name)
        self._segments.add(segment)
        return segment
