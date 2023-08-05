#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Label, LabelType, Classification, LabeledBox2D, LabeledBox3D,
LabeledPolygon2D and LabeledPolyline2D
"""

from typing import Any, Dict, Iterable, List, Optional, Sequence, TypeVar, Union

from ..geometry import Box2D, Box3D, Keypoints2D, Polygon2D, Polyline2D, Quaternion, Transform3D
from ..utility import ReprBase, ReprType, TypeClass, TypeEnum, TypeRegister

T = TypeVar("T", bound="LabeledBox3D")  # pylint: disable=invalid-name


class LabelType(TypeEnum):
    """this class defines the type of the labels.

    :param label_key: The key string of the json format label annotation
    """

    CLASSIFICATION = "labels_classification"
    BOX2D = "labels_box2D"
    BOX3D = "labels_box3D"
    POLYGON2D = "labels_polygon"
    POLYLINE2D = "labels_polyline"
    SENTENCE = "labels_sentence"
    KEYPOINTS2D = "KEYPOINTS2D"


class Label(TypeClass[LabelType], ReprBase):
    """this class defines the concept of label and some operations on it.

    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "category": <str>
        "attributes": <Dict>
        "instance": <str>
    }
    """

    _repr_type = ReprType.INSTANCE
    _repr_attributes = ("category", "attributes", "instance")

    def __init__(
        self,
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            self.category = loads.get("category", None)
            self.attributes = loads.get("attributes", None)
            self.instance = loads.get("instance", None)
        else:
            self.category = category
            self.attributes = attributes
            self.instance = instance

    def dumps(self) -> Dict[str, Any]:
        """dump a label into a dict."""

        label_dict: Dict[str, Any] = {}
        if self.category:
            label_dict["category"] = self.category
        if self.attributes:
            label_dict["attributes"] = self.attributes
        if self.instance:
            label_dict["instance"] = self.instance

        return label_dict


@TypeRegister(LabelType.CLASSIFICATION)
class Classification(Label):
    """this class defines the concept of classification label.

    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "category": <str>
        "attributes": <Dict>
        "instance": <str>
    }
    """


@TypeRegister(LabelType.BOX2D)
class LabeledBox2D(Box2D, Label):  # pylint: disable=too-many-ancestors
    """Contain the definition of LabeledBox2D bounding box and some related operations.

    :param args: Union[None, float, Sequence[float]],
        box = LabeledBox2D()
        box = LabeledBox2D(10, 20, 30, 40)
        box = LabeledBox2D([10, 20, 30, 40])
    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "box2D": <List[Dict]>
        "category": <str>
        "attributes": <Dict>
        "instance": <str>
    }
    :param x: X coordinate of the top left vertex of the box
    :param y: Y coordinate of the top left vertex of the box
    :param width: Length along the x axis
    :param height: Length along the y axis
    """

    _repr_type = ReprType.INSTANCE
    _repr_attributes = Label._repr_attributes

    def __init__(
        self,
        *args: Union[None, float, Sequence[float]],
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ):
        if loads:
            Box2D.__init__(self, loads=loads["box2D"])
            Label.__init__(self, loads=loads)
        else:
            Box2D.__init__(self, *args, loads=None, x=x, y=y, width=width, height=height)
            Label.__init__(self, category, attributes, instance)

    def dumps(self) -> Dict[str, Any]:  # type: ignore[override]
        labeled_box2d_dict = Label.dumps(self)
        labeled_box2d_dict["box2D"] = Box2D.dumps(self)
        return labeled_box2d_dict


@TypeRegister(LabelType.BOX3D)
class LabeledBox3D(Box3D, Label):
    """Contain the definition of LabeledBox3D bounding box and some related operations.

    :param transform: A Transform3D object or a 4x4 or 3x4 transfrom matrix
    :param translation: Translation in a sequence of [x, y, z]
    :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or `Quaternion`
    :param size: Size in a sequence of [x, y, z]
    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "translation": translation in a sequence of [x, y, z]
        "rotation": rotation in a sequence of [w, x, y, z]
        "size": size in a sequence of [x, y, z]
        "category": <str>
        "attributes": <Dict>
        "instance": <str>
    }
    :param kwargs: Other parameters to initialize rotation of the transform
    """

    _repr_attributes = Box3D._repr_attributes + Label._repr_attributes  # type: ignore[assignment]

    def __init__(
        self,
        transform: Transform3D.TransformType = None,
        *,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        size: Optional[Sequence[float]] = None,
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
        **kwargs: Quaternion.KwargsType,
    ):
        if loads:
            Box3D.__init__(self, loads=loads["box3D"])
            Label.__init__(self, loads=loads)
            return

        Box3D.__init__(
            self,
            transform,
            translation=translation,
            rotation=rotation,
            size=size,
            loads=None,
            **kwargs,
        )
        Label.__init__(self, category, attributes, instance)

    def __rmul__(self: T, other: Transform3D) -> T:
        if isinstance(other, Transform3D):
            labeled_box_3d = Box3D.__rmul__(self, other)
            labeled_box_3d.category = self.category
            labeled_box_3d.attributes = self.attributes
            labeled_box_3d.instance = self.instance
            return labeled_box_3d

        return NotImplemented  # type: ignore[unreachable]

    def dumps(self) -> Dict[str, Any]:
        labeled_box3d_dict = Label.dumps(self)
        labeled_box3d_dict["box3D"] = Box3D.dumps(self)
        return labeled_box3d_dict

    def get_repr_str(self) -> str:
        """return basic info of the Label.

        :return: basic info of the Label
        """
        return f"{self.__class__.__name__}"


@TypeRegister(LabelType.POLYGON2D)
class LabeledPolygon2D(Polygon2D, Label):  # pylint: disable=too-many-ancestors
    """this class defines the polygon2D with labels

    :param points: a list of 2D point list
    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "polygon": [
            { "x": <int>
              "y": <int>
            },
            ...
            ...
        ],
        "category": <str>
        "attributes": {
            "<key>": "<value>" <str>
            ...
            ...
        }
        "instance": <str>
    }
    """

    def __init__(
        self,
        points: Optional[Sequence[Sequence[float]]] = None,
        *,
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            super().__init__(loads=loads["polygon"])
            Label.__init__(self, loads=loads)
        else:
            super().__init__(points)
            Label.__init__(self, category, attributes, instance)

    def dumps(self) -> Dict[str, Any]:  # type: ignore[override]
        """dump a LabeledPolygon2D into a dict"""

        data = Label.dumps(self)
        data["polygon"] = super().dumps()

        return data

    def get_repr_str(self) -> str:
        """return basic info of the Label.

        :return: basic info of the Label
        """
        return f"{type(self).__name__}"


@TypeRegister(LabelType.POLYLINE2D)
class LabeledPolyline2D(Polyline2D, Label):  # pylint: disable=too-many-ancestors
    """this class defines the polyline2D with labels

    :param points: a list of 2D point list
    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "polyline": [
            { "x": <int>
              "y": <int>
            },
            ...
            ...
        ],
        "category": <str>
        "attributes": {
            "<key>": "<value>" <str>
            ...
            ...
        }
        "instance": <str>
    }
    """

    def __init__(
        self,
        points: Optional[Sequence[Sequence[float]]] = None,
        *,
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            super().__init__(loads=loads["polyline"])
            Label.__init__(self, loads=loads)
        else:
            super().__init__(points)
            Label.__init__(self, category, attributes, instance)

    def dumps(self) -> Dict[str, Any]:  # type: ignore[override]
        """dump a LabeledPolyline2D into a dict"""

        data = Label.dumps(self)
        data["polyline"] = super().dumps()

        return data


class Word:
    """Contain the content and time of the word

    :param text: content of the word
    :param begin: the begin time of the word in audio
    :param end: the end time of the word in audio
    :loads : {
        "text": str ,
        "begin": fload,
        "end": fload,
    }
    """

    def __init__(
        self,
        text: Optional[str] = None,
        begin: Optional[float] = None,
        end: Optional[float] = None,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            self._text: str = loads["text"]
            self._begin: Optional[float] = loads.get("begin", None)
            self._end: Optional[float] = loads.get("end", None)
            return
        if not text:
            raise TypeError("Require a text to construct a Word.")
        self._text = text
        self._begin = begin
        self._end = end

    @property
    def text(self) -> str:
        """Return the text of the Word."""
        return self._text

    @property
    def begin(self) -> Optional[float]:
        """Return the begin time of the word"""
        return self._begin

    @property
    def end(self) -> Optional[float]:
        """Return the end time of the word"""
        return self._end

    def dumps(self) -> Dict[str, Any]:
        """Dumps a word into a dict"""
        data: Dict[str, Any] = {"text": self._text}
        if self._begin:
            data["begin"] = self._begin
        if self._end:
            data["end"] = self._end
        return data


@TypeRegister(LabelType.SENTENCE)  # pylint: disable=too-few-public-methods
class LabeledSentence(Label):
    """this class defines the speech to sentence with lables

    :param sentence: a list of sentence
    :param speech: a list of spell, only exists in chinese language
    :param phone: a list of phone
    :param attributes: attributes of the label
    :param loads:{
        "sentence": [
            {
                "text":         <string>
                "begin":         <number>
                "end":           <number>
            }
            ...
            ...
        ],
        "spell": [
            {
                "text":          <string>
                "begin":         <number>
                "end":           <number>
            }
            ...
            ...
        ],
        "phone": [
            {
                "text":          <string>
                "begin":         <number>
                "end":           <number>
            }
            ...
            ...
        ],
        "attributes": {
            <key>: <value>,    <str>
            ...
            ...
        }
    }
    """

    def __init__(
        self,
        sentence: Optional[Iterable[Word]] = None,
        spell: Optional[Iterable[Word]] = None,
        phone: Optional[Iterable[Word]] = None,
        *,
        attributes: Optional[Dict[str, Any]] = None,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            super().__init__(loads=loads)
            self._sentence = self._load_word(loads.get("sentence", []))
            self._spell = self._load_word(loads.get("spell", []))
            self._phone = self._load_word(loads.get("phone", []))
        else:
            super().__init__(attributes=attributes)
            self._sentence = list(sentence) if sentence else []
            self._spell = list(spell) if spell else []
            self._phone = list(phone) if phone else []

    @staticmethod
    def _load_word(words: List[Dict[str, Any]]) -> List[Word]:
        return [Word(loads=word) for word in words]

    def dumps(self) -> Dict[str, Any]:
        """dump a LabeledSentence into a dict"""

        data = Label.dumps(self)
        if self._sentence:
            data["sentence"] = [word.dumps() for word in self._sentence]
        if self._spell:
            data["spell"] = [word.dumps() for word in self._spell]
        if self._phone:
            data["phone"] = [word.dumps() for word in self._phone]
        return data


@TypeRegister(LabelType.KEYPOINTS2D)
class LabeledKeypoints2D(Keypoints2D, Label):  # pylint: disable=too-many-ancestors
    """This class defines Keypoints2D with labels.

    :param keypoints: a list of 2D keypoint list
    :param category: Category of the label
    :param attributes: Attributs of the label
    :param instance: Labeled instance
    :param loads: {
        "keypoints2d": [
            { "x": <float>
              "y": <float>
              "v": <int>
            },
            ...
            ...
        ],
        "category": <str>
        "attributes": {
            "<key>": "<value>" <str>
            ...
            ...
        }
        "instance": <str>
    }
    """

    _repr_type = ReprType.INSTANCE
    _repr_attributes = Label._repr_attributes

    def __init__(
        self,
        keypoints: Optional[Sequence[Sequence[float]]],
        *,
        category: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        if loads:
            super().__init__(loads=loads["keypoints2d"])
            Label.__init__(self, loads=loads)
        else:
            super().__init__(keypoints)
            Label.__init__(self, category, attributes, instance)

    def _repr_head(self) -> str:
        return f"{self.__class__.__name__}{self._data}"

    def dumps(self) -> Dict[str, Any]:  # type: ignore[override]
        """Dumps a LabeledKeypoints2D into a dict

        :return: a dictionary containing the labeled 2D keypoints
        """
        data = Label.dumps(self)
        data["keypoints2d"] = super().dumps()

        return data
