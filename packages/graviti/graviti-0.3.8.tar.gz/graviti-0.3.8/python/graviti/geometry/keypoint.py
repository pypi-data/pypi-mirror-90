#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Keypoints2D and Keypoint2D."""

from typing import Dict, Optional, Sequence, Type, TypeVar, Union

from .polygon import PointList2D
from .vector import Vector2D

_T = TypeVar("_T", bound=Vector2D)


class Keypoint2D(Vector2D):
    """A class used to represent 2D keypoint.

    :param args: coordinates and visible status(optional) of the 2D keypoint
    :param loads: a dicitionary containing the 2D keypoint coordinates and visible status(optional)
    :param kwargs: coordinates are float type and visible status is int type
        keypoint2d = Keypoint2D(x=1.0, y=2.0)
        keypoint2d = Keypoint2D(x=1.0, y=2.0, v=0)
        keypoint2d = Keypoint2D(x=1.0, y=2.0, v=1)
        keypoint2d = Keypoint2D(x=1.0, y=2.0, v=2)
    :raise TypeError: when input params do not meet the requirement
    """

    def __new__(
        cls: Type[_T],
        *args: Union[None, float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> _T:

        obj: _T = object.__new__(cls)
        if loads:
            kwargs = loads
        if kwargs:
            if "v" in kwargs:
                obj._data = (kwargs["x"], kwargs["y"], kwargs["v"])
            else:
                obj._data = (kwargs["x"], kwargs["y"])
            return obj

        data: Optional[Sequence[float]]
        data = args[0] if len(args) == 1 else args  # type: ignore[assignment]

        try:
            if len(data) in (2, 3):  # type: ignore[arg-type]
                obj._data = tuple(data)  # type: ignore[arg-type]
                return obj
        except TypeError:
            pass

        raise TypeError(f"Require two or three dimensional data to construct {cls.__name__}.")

    def __add__(self, other: Sequence[float]) -> Vector2D:  # type: ignore[override]
        # Result of adding Keypoint2D with another sequence should be a Vector2D.
        # Add function of Vector2D should also add support for adding with a Keypoint2D.
        # Will be implemented in the future.
        return NotImplemented

    def __neg__(self) -> Vector2D:  # type: ignore[override]
        result: Vector2D = object.__new__(Vector2D)
        result._data = tuple(-coordinate for coordinate in self._data[: self._DIMENSION])
        return result

    @property
    def v(self) -> Optional[int]:  # pylint: disable=invalid-name
        """Get the visible status of the 2D keypoint.

        :return: visible status of the 2D keypoint
        """
        if len(self._data) != self._DIMENSION:
            return self._data[2]  # type: ignore[return-value]
        return None

    def dumps(self) -> Dict[str, float]:
        """Dumps the Keypoint2D into a dictionary.

        :return: a dictionary containing the 2D keypoint coordinates and visible status(optional)
        """
        keypoint_dict = {"x": self._data[0], "y": self._data[1]}
        if len(self._data) != self._DIMENSION:
            keypoint_dict["v"] = self._data[2]
        return keypoint_dict


class Keypoints2D(PointList2D[Keypoint2D]):
    """A class used to represent 2D keypoints based on :class `PointList2D`."""

    _ElementType = Keypoint2D
