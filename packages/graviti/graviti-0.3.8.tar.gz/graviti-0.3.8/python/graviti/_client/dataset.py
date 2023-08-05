#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetClientBase, DatasetClient, FusionDatasetClient,
SegmentClientBase, SegmentClient, FusionSegmentClient
"""

from typing import Any, Dict, Generator, List, Optional, TypeVar, Union

from ..dataset import Data, Frame, FusionSegment, Segment
from ..label import Catalog
from ..sensor import Sensor
from ..utility import TBRN, NameSortedDict
from .exceptions import GASSegmentError
from .labelset import (
    FusionLabelSegmentClient,
    FusionLabelsetClient,
    LabelSegmentClient,
    LabelsetClient,
    LabelsetClientBase,
)
from .requests import Client

T = TypeVar("T", bound=Sensor)  # pylint: disable=invalid-name


class SegmentClientBase:
    """This class defines the concept of a segment client and some opertions on it.

    :param name: Segment name, unique for a dataset
    :param dataset_id: Dataset Id
    :param dataset_name: Dataset name
    :param client: The client used for sending request to TensorBay
    :param commit_id: Dataset commit ID
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        self._name = name
        self._dataset_id = dataset_id
        self._dataset_name = dataset_name
        self._client = client
        self._commit_id = commit_id

    @property
    def name(self) -> str:
        """Get the name of this segment client.

        :return: The name of the segment
        """
        return self._name

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    @property
    def commit_id(self) -> Optional[str]:
        """Get the dataset commit ID.

        :return: The dataset commit ID
        """
        return self._commit_id

    def _list_labels(self) -> Generator[Dict[str, Any], None, None]:
        """List labels in a segment client.

        :return: A generator of labels
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        while True:
            params["offset"] = offset
            response = self._client.open_api_get(
                "labels", params, dataset_id=self.dataset_id
            ).json()
            yield from response["labels"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size


class SegmentClient(SegmentClientBase):
    """ContentSegmentClient has only one sensor, supporting upload_data method."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        super().__init__(name, dataset_id, dataset_name, client, commit_id)

    def upload_data(self, local_path: str, remote_path: str = "") -> None:
        """Upload data with local path to the segment.

        :param local_path: The local path of the data to upload
        :param remote_path: The path to save the data in segment client
        :raises
            GASPathError: when remote_path does not follow linux style
            GASFrameError: when uploading frame has neither timestamp nor frame_index
        """

        self._content_segment_client.upload_data(local_path, remote_path)

    def upload_data_object(self, data: Data) -> None:
        """Upload data with local path in Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self._content_segment_client.upload_data_object(data)
        if self._content_segment_client:
            self._content_segment_client.upload_data_object(data)

    def delete_data(self, remote_paths: Union[str, List[str]]) -> None:
        """Delete data with remote paths.

        :param remote_paths: A single path or a list of paths which need to deleted,
        eg: test/os1.png or [test/os1.png]
        """
        self._content_segment_client.delete_data(remote_paths)

    def _list_data(self) -> Generator[Dict[str, Any], None, None]:
        """List data in a segment client.

        :return: A generator of data
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get("data", params, dataset_id=self.dataset_id).json()
            yield from response["data"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_data(self) -> Generator[str, None, None]:
        """List all data path in a segment client.

        :return: A generator of data path
        """
        return (item["remotePath"] for item in self._list_data())

    def list_data_objects(self) -> Generator[Data, None, None]:
        """List all `Data` object in a dataset segment.

        :return: A generator of `Data` object
        """
        for labels in self._list_labels():
            remote_path = labels["remotePath"]
            tbrn = TBRN(self._dataset_name, self._name, remote_path=remote_path)
            loads = labels["label"]
            loads["fileuri"] = tbrn
            yield Data(loads=loads)


class FusionSegmentClient(SegmentClientBase):
    """FusionSegmentClient has multiple sensors,
    supporting upload_sensor and upload_frame method.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        super().__init__(name, dataset_id, dataset_name, client, commit_id)

    def upload_sensor_object(self, sensor: T) -> None:
        """Upload sensor to the segment client.

        :param sensor: The sensor to upload
        """
        self._content_segment_client.upload_sensor_object(sensor)

    def delete_sensors(self, sensor_names: Union[str, List[str]]) -> None:
        """Delete sensors with a single name or a name list.

        :param sensor_names: A single sensor name or a list of sensor names
        """
        self._content_segment_client.delete_sensors(sensor_names)

    def _list_frames(self) -> Generator[Dict[str, Any], None, None]:
        """List all frames in a segment client(Fusion dataset).

        :return: A generator of fusion data
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get("data", params, dataset_id=self.dataset_id).json()
            yield from response["data"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_frame_objects(self) -> Generator[Frame, None, None]:
        """List all frames in the segment.

        :return: A list `Frame` object
        """
        for frame_index, labels in enumerate(self._list_labels()):
            frame = Frame()
            for data_info in labels["frame"]:
                loads = data_info["label"]
                sensor_name = data_info["sensorName"]
                remote_path = data_info["remotePath"]
                loads["timestamp"] = data_info["timestamp"]
                tbrn = TBRN(
                    self._dataset_name,
                    self._name,
                    frame_index,
                    sensor_name,
                    remote_path=remote_path,
                )
                loads["fileuri"] = tbrn
                frame[sensor_name] = Data(loads=loads)
            yield frame

    def list_sensors(self) -> List[str]:
        """List all sensor names in a segment client.

        :return: A list of sensor name
        """
        return self._content_segment_client.list_sensors()

    def list_sensor_objects(self) -> NameSortedDict[Sensor]:
        """List all sensors in a segment client.

        :return: A NameSortedDict of `Sensor` object
        """
        return self._content_segment_client.list_sensor_objects()

    def upload_frame_object(self, frame: Frame, frame_index: Optional[int] = None) -> None:
        """Upload frame to the segment client.

        :param frame: The frame to upload
        :param frame_index: The frame index, used for TensorBay to sort the frame
        :raises
            GASPathError: when remote_path does not follow linux style
        """

        self._content_segment_client.upload_frame_object(frame, frame_index)

        if self._label_segment_client:
            self._label_segment_client.upload_frame_object(frame)


class DatasetClientBase:
    """This class defines the concept of a dataset and some operations on it.

    :param name: Dataset name
    :param dataset_id: Dataset id
    :param client: The client used for sending request to TensorBay
    :param commit_id: The dataset commit Id
    """

    def __init__(
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        self._name = name
        self._dataset_id = dataset_id
        self._client = client
        self._commit_id = commit_id

    def set_description(self, description: str) -> None:
        """Set description of the dataset.

        :param description: description of the dataset
        """
        post_data = {
            "datasetId": self._dataset_id,
            "desc": description,
        }
        self._client.dataset_post("updateDataset", post_data)

    @property
    def commit_id(self) -> Optional[str]:
        """Get the dataset commit Id

        :return: The dataset commit Id
        """
        return self._commit_id

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    def _commit(self, message: str, tag: Optional[str] = None) -> str:
        post_data = {
            "message": message,
        }
        if tag:
            post_data["tag"] = tag

        response = self._client.open_api_post("", post_data, dataset_id=self.dataset_id)
        return response.json()["commitId"]  # type: ignore[no-any-return]

    def _create_segment(self, name: str) -> None:
        post_data = {"name": name}
        self._client.open_api_post("segments", post_data, dataset_id=self.dataset_id)

    def _list_segments(self) -> Generator[str, None, None]:
        offset, page_size = 0, 128
        params: Dict[str, Any] = {}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get(
                "segments", params, dataset_id=self.dataset_id
            ).json()
            yield from response["segments"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_segments(self) -> Generator[str, None, None]:
        """List all segment names in a dataset.

        :return: A generator of segment names
        """
        return self._list_segments()

    def delete_segments(
        self,
        segment_names: Union[str, List[str]],
        force_delete: bool = False,
    ) -> None:
        """Delete segments according to the name list.

        :param name: A single segment Name or a list of the segment names, if empty, the default
        segment will be deleted, if you want to delete all segment, "_all" should be submitted.
        :param force_delete: By default, only segment with no sensor can be deleted.
        If force_delete is true, then sensor and its objects will also be deleted
        """
        self._contentset_client.delete_segments(segment_names, force_delete)

    def _create_labelset(self, catalog: Catalog) -> str:
        metadata = LabelsetClientBase.create_metadata(catalog)
        if not metadata:
            raise TypeError("Empty catalog")

        post_data = {
            "datasetId": self._dataset_id,
            "contentSetId": self.contentset_id,
            "type": LabelsetClientBase.TYPE_GROUND_TRUTH,
            "version": "v1.0.2",
            "meta": metadata,
        }

        data = self._client.labelset_post("createLabelSet", post_data)
        return data["labelSetId"]  # type: ignore[no-any-return]


class DatasetClient(DatasetClientBase):
    """dataset has only one sensor, supporting create segment."""

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        super().__init__(name, dataset_id, client, commit_id)

    def get_or_create_segment(self, name: str = "_default") -> SegmentClient:
        """Create a segment set according to its name.

        :param name: Segment name, can not be "_default"
        :return: Created segment with given name, if not given name, Created default segment
        """
        if name not in self._list_segments():
            self._create_segment(name)
        return SegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment(self, name: str = "_default") -> SegmentClient:
        """Get a segment according to its name.

        :param name: The name of the desired segment
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment
        """
        if name not in self._list_segments():
            raise GASSegmentError(name)

        return SegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment_object(self, name: str = "_default") -> Segment:
        """Get a segment object according to its name.

        :param name: The name of the desired segment object
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment object
        """
        segment_client = self.get_segment(name)
        segment = Segment(name)
        for data in segment_client.list_data_objects():
            segment.append(data)

        return segment

    def upload_segment_object(
        self,
        segment: Segment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> SegmentClient:
        """Upload a `Segment` to the dataset,
        This function will upload all info contains in the input `Segment` object,
        which includes:
        - Create a segment using the name of input `Segment`
        - Upload all `Data` in the Segment to the dataset

        :param segment: The `Segment` object contains the information needs to be upload
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `Segment`
        """
        content_segment_client = self._contentset_client.upload_segment_object(
            segment,
            jobs=jobs,
            skip_uploaded_files=skip_uploaded_files,
        )
        label_segment_client: Optional[LabelSegmentClient] = None
        if self._labelset_client:
            label_segment_client = self._labelset_client.upload_segment_object(
                segment,
                jobs=jobs,
                skip_uploaded_files=skip_uploaded_files,
            )

        return SegmentClient(
            segment.name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def upload_catalog(self, catalog: Catalog) -> None:
        """Upload a Catalog to the dataset,

        :param catalog: The `Catalog` object to upload
        """
        if not self._labelset_client:
            labelset_id = self._create_labelset(catalog)
            self._labelset_client = LabelsetClient(labelset_id, self._name, self._client)
            return

        self._labelset_client.upload_catalog(catalog, self.dataset_id)

    def commit(self, message: str, tag: Optional[str] = None) -> "DatasetClient":
        """
        Commit dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed dataset client
        """
        commit_id = self._commit(message, tag)
        return DatasetClient(self._name, self.dataset_id, self._client, commit_id)


class FusionDatasetClient(DatasetClientBase):
    """Client for fusion dataset which has multiple sensors,
    supporting create fusion segment.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        super().__init__(name, dataset_id, client, commit_id)

    def get_or_create_segment(self, name: str = "_default") -> FusionSegmentClient:
        """Create a fusion segment set according to the given name.

        :param name: Segment name, can not be "_default"
        :return: Created fusion segment with given name, if not given name, Created default segment
        """
        if name not in self._list_segments():
            self._create_segment(name)
        return FusionSegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment(self, name: str = "_default") -> FusionSegmentClient:
        """Get a fusion segment according to its name.

        :param name: The name of the desired fusion segment
        :raises GASSegmentError: When the required fusion segment does not exist
        :return: The desired fusion segment
        """
        if name not in self._list_segments():
            raise GASSegmentError(name)
        return FusionSegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def upload_segment_object(
        self,
        segment: FusionSegment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionSegmentClient:
        """Upload a `FusionSegment` to the dataset,
        This function will upload all info contains in the input `FusionSegment` object,
        which includes:
        - Create a segment using the name of input `FusionSegment`
        - Upload all `Sensor` in the segment to the dataset
        - Upload all `Frame` in the segment to the dataset

        :param segment: The `Segment` object needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `FusionSegment`
        """
        content_segment_client = self._contentset_client.upload_segment_object(
            segment,
            jobs=jobs,
            skip_uploaded_files=skip_uploaded_files,
        )
        label_segment_client: Optional[FusionLabelSegmentClient] = None
        if self._labelset_client:
            label_segment_client = self._labelset_client.upload_segment_object(
                segment,
                jobs=jobs,
                skip_uploaded_files=skip_uploaded_files,
            )

        return FusionSegmentClient(
            segment.name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def upload_catalog(self, catalog: Catalog) -> None:
        """Upload a Catalog to the fusion dataset,

        :param catalog: The `Catalog` object to upload
        """
        if not self._labelset_client:
            labelset_id = self._create_labelset(catalog)
            self._labelset_client = FusionLabelsetClient(labelset_id, self._name, self._client)
            return

        self._labelset_client.upload_catalog(catalog, self.dataset_id)

    def commit(self, message: str, tag: Optional[str] = None) -> "FusionDatasetClient":
        """
        Commit fusion dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed fusion dataset client
        """
        commit_id = self._commit(message, tag)
        return FusionDatasetClient(self._name, self.dataset_id, self._client, commit_id)
