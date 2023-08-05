#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class CatagoryInfo, AttributeInfo and Subcatalog."""

from enum import Enum, auto
from typing import (
    Any,
    Dict,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    ValuesView,
    overload,
)

from typing_extensions import Literal

from ..utility import NameClass, NameOrderedDict, ReprBase, ReprType
from .label import LabelType


class AttributeType(Enum):
    """All the possible type of the attributes."""

    boolean = bool
    integer = int
    number = float
    string = str
    null = None
    instance = "instance"


class CategoryInfo(NameClass):
    """Information of a category, includes category name and description

    :param name: The name of the category
    :param loads: A dict contains all information of the category
    :raises
        TypeError: Name is required when not given loads
    """


class AttributeInfo(NameClass):
    """Information of an attribute

    :param name: The name of the attribute
    :param enum: All the possible values of the attribute
    :param attribute_type: The type of the attribute value
    :param minimum: The minimum value of number type attribute
    :param maximum: The maximum value of number type attribute
    :is_array: Whether the attribute is a sequence of values or not
    :param parent_categories: The parent categories of the attribute
    :param loads: A dict contains all information of the attribute
    :raises
        TypeError: Name and values are required when not given loads
    """

    SingleArgType = Union[
        str,
        None,
        Type[Any],
        AttributeType,
    ]
    ArgType = Union[SingleArgType, Iterable[SingleArgType]]

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        enum: Optional[Iterable[str]] = None,
        attribute_type: Optional[ArgType] = None,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        is_array: bool = False,
        parent_categories: Union[None, str, Iterable[str]] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            super().__init__(loads=loads)
            self._parent_categories: List[str] = loads.get("parentCategories", [])
            if loads.get("type", None) == "array":
                self._is_array = True
                schema = loads["items"]
            else:
                self._is_array = False
                schema = loads

            self._enum: Optional[List[str]] = schema.get("enum", None)
            self._type: Union[AttributeType, List[AttributeType], None] = self._convert_type(
                schema.get("type", None)
            )
            self._minimum: Optional[float] = schema.get("minimum", None)
            self._maximum: Optional[float] = schema.get("maximum", None)
            return

        super().__init__(name)

        self._enum = list(enum) if enum else None
        self._type = self._convert_type(attribute_type)
        self._minimum = minimum
        self._maximum = maximum
        self._is_array = is_array

        if not parent_categories:
            self._parent_categories = []
        elif isinstance(parent_categories, str):
            self._parent_categories = [parent_categories]
        else:
            self._parent_categories = list(parent_categories)

    def _convert_type(self, type_: ArgType) -> Union[AttributeType, List[AttributeType], None]:
        if not type_:
            return None

        if isinstance(type_, Iterable) and not isinstance(type_, str):  # pylint: disable=W1116
            return [self._convert_single_type(single_type) for single_type in type_]

        return self._convert_single_type(type_)

    @staticmethod
    def _convert_single_type(type_: Union[str, Type[Any], AttributeType, None]) -> AttributeType:
        if isinstance(type_, str):
            return AttributeType[type_]

        if isinstance(type_, AttributeType):
            return type_

        return AttributeType(type_)

    def _dump_type(self) -> Union[str, List[str], None]:
        if isinstance(self._type, list):
            return [type_.name for type_ in self._type]

        if self._type:
            return self._type.name

        return None

    @property
    def enum(self) -> Optional[List[str]]:
        """Get the enum values of the attribute.

        :return: The enum values of the attribute
        """
        return self._enum

    @property
    def attribute_type(self) -> Union[AttributeType, List[AttributeType], None]:
        """Get the type of the attribute.

        :return: The type of the attribute
        """
        return self._type

    @property
    def minimum(self) -> Optional[float]:
        """Get the minimum value of the attribute.

        :return: The minimum value of the attribute
        """
        return self._minimum

    @property
    def maximum(self) -> Optional[float]:
        """Get the maximum value of the attribute.

        :return: The maximum value of the attribute
        """
        return self._maximum

    @property
    def is_array(self) -> bool:
        """Get if the type of the attribute is array.

        :return: A bool value indicating whether the type of the attribute is array
        """
        return self._is_array

    @property
    def parent_categories(self) -> List[str]:
        """Get the parent categories of the attribute.

        :return: The parent categories of the attribute
        """
        return self._parent_categories

    def dumps(self) -> Dict[str, Any]:
        """Dumps the information of this attribute as a dictionary.

        :return: A dictionary contains all information of this attribute
        """
        schema: Dict[str, Any] = {}
        if self._type:
            schema["type"] = self._dump_type()
        if self._enum:
            schema["enum"] = self._enum
        if self._minimum is not None:
            schema["minimum"] = self._minimum
        if self._maximum is not None:
            schema["maximum"] = self._maximum

        data: Dict[str, Any] = super().dumps()
        if self._is_array:
            data["type"] = "array"
            data["items"] = schema
        else:
            data.update(schema)
        if self._parent_categories:
            data["parentCategories"] = self._parent_categories
        return data


class SubcatalogBase:  # pylint: disable=too-few-public-methods
    """This class defines the concept of a subcatalog.

    :param loads: A dict contains attributes of the subcatalog
    """

    def __init__(self, *, loads: Optional[Dict[str, Any]] = None) -> None:

        self._attributes: NameOrderedDict[AttributeInfo] = NameOrderedDict()
        if loads:
            for attribute in loads.get("attributes", []):
                self.add_attribute(loads=attribute)

    @property
    def attributes(self) -> NameOrderedDict[AttributeInfo]:
        """Return all the attributes of the Subcatalog.

        :return: A NameOrderedDict of all the attributes
        """
        return self._attributes

    def dump_attributes(self) -> List[Dict[str, Any]]:
        """Dump all the attributes as a list.

        :return: A list of dict contains all the attributes
        """
        return [attribute.dumps() for attribute in self._attributes.values()]

    def add_attribute(
        self,
        name: Optional[str] = None,
        *,
        enum: Optional[Iterable[str]] = None,
        attribute_type: Optional[AttributeInfo.ArgType] = None,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        is_array: bool = False,
        parent_categories: Union[None, str, Iterable[str]] = None,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a attribute to the Catalog

        :param name: The name of the attribute
        :param enum: All the possible values of the attribute
        :param attribute_type: The type of the attribute value
        :param minimum: The minimum value of number type attribute
        :param maximum: The maximum value of number type attribute
        :is_array: Whether the attribute is a sequence of values or not
        :param parent_categories: The parent categories of the attribute
        :param loads: A dict contains all information of the attribute
        """
        self._attributes.append(
            AttributeInfo(
                name,
                enum=enum,
                attribute_type=attribute_type,
                minimum=minimum,
                maximum=maximum,
                is_array=is_array,
                parent_categories=parent_categories,
                loads=loads,
            )
        )


class Subcatalog(SubcatalogBase):
    """A subcatalog contains all labels in a specific label type

    :param is_tracking: A boolean value indicates whether corresponding
        subcatalog is tracking related
    :param loads: A dict contains all information of the subcatalog
    """

    def __init__(
        self, is_tracking: bool = False, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(loads=loads)
        self._categories: NameOrderedDict[CategoryInfo] = NameOrderedDict()

        if loads:
            self.is_tracking: bool = loads.get("isTracking", False)
            self.description: Optional[str] = loads.get("description", None)
            for category in loads.get("categories", []):
                self.add_category(loads=category)
            return

        self.is_tracking = is_tracking
        self.description = None

    def __repr__(self) -> str:
        str_list = [f"{self.__class__.__name__}["]

        for category in self._categories.values():
            str_list.append(f"  {str(category)},")

        for attribute in self._attributes.values():
            str_list.append(f"  {str(attribute)},")

        str_list.append("]")

        return "\n".join(str_list)

    @property
    def categories(self) -> NameOrderedDict[CategoryInfo]:
        """Return all the categories of the Subcatalog.

        :return: A NameOrderedDict of all the categories
        """
        return self._categories

    def dump_categories(self) -> List[Dict[str, Any]]:
        """Dump all the categories as a list.

        :return: A list of dict contains all the categories
        """
        return [category.dumps() for category in self._categories.values()]

    def dumps(self) -> Dict[str, Any]:
        """Dumps the information of this Subcatalog into a dictionary.

        :return: A dictionary contains all information of this Subcatalog
        """
        data: Dict[str, Any] = {}

        if self.is_tracking:
            data["isTracking"] = self.is_tracking
        if self.description:
            data["description"] = self.description
        if self._categories:
            data["categories"] = self.dump_categories()
        if self._attributes:
            data["attributes"] = self.dump_attributes()

        return data

    def add_category(
        self, name: Optional[str] = None, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a category to the Subcatalog

        :param name: The name of the category
        :param loads: A dict contains all information of the category
        """
        self._categories.append(CategoryInfo(name, loads=loads))


class AudioSubcatalog(SubcatalogBase):
    """A subcatalog contains all audio label type

    :param is_sample: A boolen value indicates whether time format is sample related
    :param sample_rate: The number of samples of audio carried per second
    :param lexicon: A list consists all of text and phone
    :param loads: A dict contains all information of the SubCatalog
    """

    def __init__(
        self,
        is_sample: bool = False,
        sample_rate: Optional[int] = None,
        lexicon: Optional[List[List[str]]] = None,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:

        super().__init__(loads=loads)
        if loads:
            self.is_sample: bool = loads.get("isSample", False)
            self.sample_rate: Optional[int] = loads.get("sampleRate", None)
            self._lexicon: List[List[str]] = loads.get("lexicon", [])
            self.description: Optional[str] = loads.get("description", None)
            return
        self.is_sample = is_sample
        self.sample_rate = sample_rate
        self._lexicon = lexicon if lexicon else []
        self.description = None

    def __repr__(self) -> str:
        str_list = [f"{self.__class__.__name__}["]
        if self.is_sample:
            str_list.append(f"is_sample: {self.is_sample}")
        if self.sample_rate:
            str_list.append(f"sample_rate: {self.sample_rate}")

        for attribute in self._attributes.values():
            str_list.append(f"  {str(attribute)},")

        str_list.append("]")

        return "\n".join(str_list)

    @property
    def lexicon(self) -> List[List[str]]:
        """Retun the lexicon

        :return: A list of all lexicon
        """
        return self._lexicon

    def dumps(self) -> Dict[str, Any]:
        """Dumps the information of this AudioSubcatalog into a dictionary.

        :return: A dictionary contains all information of this AudioSubCatalog
        """
        data: Dict[str, Any] = {}

        attributes = [attribute.dumps() for attribute in self._attributes.values()]

        if self.is_sample:
            data["isSample"] = self.is_sample
        if self.sample_rate:
            data["sampleRate"] = self.sample_rate
        if self.description:
            data["description"] = self.description
        if self._lexicon:
            data["lexicon"] = self._lexicon
        if attributes:
            data["attributes"] = attributes

        return data

    def append_lexicon(self, lexemes: List[str]) -> None:
        """Add lexemes to lexicon

        :param: A list consists of text and phone
        """
        self._lexicon.append(lexemes)


class VisibleType(Enum):
    """All the possible visible types of keypoints labels."""

    TERNARY = auto()
    BINARY = auto()


class KeypointsInfo(ReprBase):
    """Information of a type of keypoints label.

    :param number: The number of keypoints
    :param names: All the names of keypoints
    :param skeleton: The skeleton of keypoints
    :param visible: The visible type of keypoints
    :param parent_categories: The parent categories of the keypoints
    :param description: The description of keypoints
    :param loads: A dict contains all information of the keypoints
    :raises
        TypeError: Number is required when not given loads
    """

    _repr_type = ReprType.INSTANCE
    _repr_attributes = (
        "number",
        "names",
        "skeleton",
        "visible",
        "parent_categories",
        "description",
    )

    def __init__(
        self,
        number: Optional[int] = None,
        *,
        names: Optional[Iterable[str]] = None,
        skeleton: Optional[Sequence[Sequence[int]]] = None,
        visible: Optional[VisibleType] = None,
        parent_categories: Union[None, str, Iterable[str]] = None,
        description: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            self._parent_categories: List[str] = loads.get("parentCategories", [])
            self._names: Optional[List[str]] = loads.get("names", None)
            skeleton = loads.get("skeleton", None)
            self._skeleton: Optional[List[Tuple[int, int]]] = (
                [tuple(line) for line in skeleton] if skeleton else None  # type: ignore[misc]
            )
            self._visible: Optional[VisibleType] = loads.get("visible", None)
            self._description: Optional[str] = loads.get("description", None)
            return

        if number is None:
            raise ValueError(f"Require number to initialize {self.__class__.__name__}")
        self._number = number
        self._names = list(names) if names else None
        self._skeleton = (
            [tuple(line) for line in skeleton] if skeleton else None  # type: ignore[misc]
        )
        self._visible = visible
        self._description = description

        if not parent_categories:
            self._parent_categories = []
        elif isinstance(parent_categories, str):
            self._parent_categories = [parent_categories]
        else:
            self._parent_categories = list(parent_categories)

    @property
    def number(self) -> int:
        """Get the number of the keypoints.

        :return: The number of the keypoints
        """
        return self._number

    @property
    def names(self) -> Optional[List[str]]:
        """Get the names of the keypoints.

        :return: The names of the keypoints
        """
        return self._names

    @property
    def skeleton(self) -> Optional[List[Tuple[int, int]]]:
        """Get the skeleton of the keypoints.

        :return: The skeleton of the keypoints
        """
        return self._skeleton

    @property
    def visible(self) -> Optional[VisibleType]:
        """Get the VisibleType of the keypoints.

        :return: The visible type of the keypoints
        """
        return self._visible

    @property
    def parent_categories(self) -> List[str]:
        """Get the parent categories of the keypoints.

        :return: the parent categories of the keypoints
        """
        return self._parent_categories

    def dumps(self) -> Dict[str, Any]:
        """Dump all the keypoint information into a dictionary.

        :return: A dictionary contains all information of the keypoint
        """
        data: Dict[str, Any] = {"number": self._number}
        if self._names:
            data["names"] = self._names
        if self._skeleton:
            data["skeleton"] = self._skeleton
        if self._visible:
            data["visible"] = self._visible.name
        if self._parent_categories:
            data["parentCategories"] = self._parent_categories
        if self._description:
            data["description"] = self._description
        return data


class KeypointsSubcatalog(Subcatalog):
    """A subcatalog contains all keypoints labels.

    :param is_tracking: A boolean value indicates whether corresponding
        keypointssubcatalog is tracking related
    :param loads: A dict contains all information of the keypointssubcatalog
    """

    def __init__(
        self, is_tracking: bool = False, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(is_tracking, loads=loads)

        self._keypoints: List[KeypointsInfo] = []
        if loads:
            for keypoint in loads["keypoints"]:
                self.add_keypoints_info(loads=keypoint)

    def __repr__(self) -> str:
        str_list = [f"{self.__class__.__name__}["]

        for category in self._categories.values():
            str_list.append(f"  {str(category)},")

        for attribute in self._attributes.values():
            str_list.append(f"  {str(attribute)},")

        for keypoint in self._keypoints:
            str_list.append(f"  {str(keypoint)},")

        str_list.append("]")
        return "\n".join(str_list)

    def add_keypoints_info(
        self,
        number: Optional[int] = None,
        *,
        names: Optional[Iterable[str]] = None,
        skeleton: Optional[Sequence[Sequence[int]]] = None,
        visible: Optional[VisibleType] = None,
        parent_categories: Union[None, str, Iterable[str]] = None,
        description: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a type of keypoints to the subcatalog.

        :param number: The number of keypoints
        :param names: All the names of keypoints
        :param skeleton: The skeleton of keypoints
        :param visible: The visible type of keypoints
        :param parent_categories: The parent categories of the keypoints
        :param description: The description of keypoints
        :param loads: A dict contains all information of the keypoints
        """
        self._keypoints.append(
            KeypointsInfo(
                number=number,
                names=names,
                skeleton=skeleton,
                visible=visible,
                parent_categories=parent_categories,
                description=description,
                loads=loads,
            )
        )

    @property
    def keypoints_info(self) -> List[KeypointsInfo]:
        """Get the KeypointsInfo of the Subcatalog.

        :return: A list of KeypointsInfo
        """
        return self._keypoints

    def dumps(self) -> Dict[str, Any]:
        """Dumps all the information of the keypoints into a dictionary

        :return: A dictionary contains all the information of this KeypointsSubcatalog
        """

        keypoints_dict: Dict[str, Any] = super().dumps()
        if self._keypoints:
            keypoints_dict["keypoints"] = [keypoint.dumps() for keypoint in self._keypoints]
        return keypoints_dict


Subcatalogs = Union[Subcatalog, AudioSubcatalog]


class Catalog(Mapping[LabelType, Subcatalogs]):
    """Catalog is a mapping which contains `Subcatalog`,
    the corresponding key is the 'name' of `LabelType`.

    :param loads: A dict contains a series of Subcatalog dicts

    """

    def __init__(self, *, loads: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        self._data: Dict[LabelType, Subcatalogs] = {}

        if loads:
            for type_name, subcatalog in loads.items():
                label_type = LabelType[type_name]
                if label_type == LabelType.SENTENCE:
                    self._data[label_type] = AudioSubcatalog(loads=subcatalog)
                else:
                    self._data[label_type] = Subcatalog(loads=subcatalog)
            return

    @overload
    def __getitem__(
        self,
        key: Literal[
            LabelType.CLASSIFICATION,
            LabelType.BOX2D,
            LabelType.BOX3D,
            LabelType.POLYGON2D,
            LabelType.POLYLINE2D,
        ],
    ) -> Subcatalog:
        ...

    @overload
    def __getitem__(self, key: Literal[LabelType.SENTENCE]) -> AudioSubcatalog:
        ...

    @overload
    def __getitem__(self, key: LabelType) -> Subcatalogs:
        ...

    def __getitem__(self, key: LabelType) -> Subcatalogs:
        return self._data.__getitem__(key)

    def __len__(self) -> int:
        return self._data.__len__()

    def __iter__(self) -> Iterator[LabelType]:
        return self._data.__iter__()

    def __repr__(self) -> str:
        str_list = [f"{self.__class__.__name__}{{"]

        for label_type in self._data:
            str_list.append(f"  {label_type.name},")

        str_list.append("}")
        return "\n".join(str_list)

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
    def create_subcatalog(self, label_type: Literal[LabelType.SENTENCE]) -> AudioSubcatalog:
        ...

    @overload
    def create_subcatalog(self, label_type: Literal[LabelType.KEYPOINTS2D]) -> KeypointsSubcatalog:
        ...

    @overload
    def create_subcatalog(self, label_type: LabelType) -> Subcatalogs:
        ...

    def create_subcatalog(
        self,
        label_type: LabelType,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> Subcatalogs:
        """Create a new subcatalog and add it to catalog.

        :param label_type: the label type of the subcatalog
        :param loads: A dict contains all information of the subcatalog

        :return: created new subcatalog
        """
        subcatalog: Subcatalogs
        if label_type == LabelType.SENTENCE:
            subcatalog = AudioSubcatalog(loads=loads)
        elif label_type == LabelType.KEYPOINTS2D:
            subcatalog = KeypointsSubcatalog(loads=loads)
        else:
            subcatalog = Subcatalog(loads=loads)

        self._data[label_type] = subcatalog
        return subcatalog

    def keys(self) -> KeysView[LabelType]:
        """Return keys view of the catalog's keys

        :return: keys view
        """
        return self._data.keys()

    def values(self) -> ValuesView[Subcatalogs]:
        """Return values view of the catalog's values.

        :return: values view
        """
        return self._data.values()

    def items(self) -> ItemsView[LabelType, Subcatalogs]:
        """Return items view of the catalog's items.

        :return: items view
        """
        return self._data.items()

    def dumps(self) -> Dict[str, Any]:
        """Dump the catalog into a series of subcatalog dict.

        :return: a dict contains a series of subcatalog dict with their label types as dict keys
        """
        subcatalog_dicts: Dict[str, Any] = {}
        for label_type, subcatalog in self._data.items():
            subcatalog_dicts[label_type.name] = subcatalog.dumps()
        return subcatalog_dicts
