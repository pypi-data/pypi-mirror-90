#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file define class Client and function read_data_from_file.
"""

import logging
import time
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar
from urllib.parse import urljoin

import requests

from .exceptions import GASRequestError, GASResponseError

logger = logging.getLogger(__name__)
JSON_CONTENT_TYPE = "application/json"


class Config:  # pylint: disable=too-few-public-methods
    """This is a base class defining the concept of Post Config

    :param max_retries: max retries of the post request
    :param timeout: timeout of the post request
    :param is_intern: whether the post request is from intern
    """

    def __init__(self, max_retries: int = 3, timeout: int = 15, is_intern: bool = False) -> None:

        self.max_retries = max_retries
        self.timeout = timeout
        self._is_intern = is_intern

    @property
    def is_intern(self) -> bool:
        """Return whether the post request is from intern.

        :return: whether the post request is from intern
        """
        return self._is_intern


default_config = Config()


class Client:
    """This is a base class defining the concept of Client,
    which contains functions to send post to content store and labelset store

    :param access_key: user's access key
    :param url: the url of the graviti gas website
    """

    _DEFAULT_URL_CN = "https://gas.graviti.cn/"
    _DEFAULT_URL_COM = "https://gas.graviti.com/"

    def __init__(self, access_key: str, url: str = "") -> None:
        if access_key.startswith("Accesskey-"):
            url = url if url else Client._DEFAULT_URL_CN
        elif access_key.startswith("ACCESSKEY-"):
            url = url if url else Client._DEFAULT_URL_COM
        else:
            raise TypeError("Wrong accesskey format!")

        self.gateway_url = urljoin(url, "gatewayv2/")
        self.access_key = access_key

        self._open_api = urljoin(self.gateway_url, "tensorbay-open-api/v1/")

    def open_api_post(self, method: str, post_data: Dict[str, Any], dataset_id: str = "") -> Any:
        """Send a POST request to the TensorBay Dataset open API

        :param method: The method of the request
        :param post_data: Json data to send in the body of the request
        :param dataset_id: Dataset id
        :return: Response of the request
        """
        if dataset_id:
            dataset_url = urljoin(self._open_api, "datasets/")
            if method:
                url = urljoin(urljoin(dataset_url, dataset_id + "/"), method)
            else:
                url = urljoin(dataset_url, dataset_id)
        else:
            url = urljoin(self._open_api, "datasets")
        return post(
            url, json_data=post_data, access_key=self.access_key, content_type=JSON_CONTENT_TYPE
        )

    def open_api_get(
        self, method: str, params: Optional[Dict[str, Any]] = None, dataset_id: str = ""
    ) -> Any:
        """Send a GET request to the TensorBay Dataset open API

        :param method: The method of the request
        :param params: Data to send in the params of the request
        :param dataset_id: Dataset id
        :return: Response of the request
        """
        if dataset_id:
            dataset_url = urljoin(self._open_api, "datasets/")
            if method:
                url = urljoin(urljoin(dataset_url, dataset_id + "/"), method)
            else:
                url = urljoin(dataset_url, dataset_id)
        else:
            url = urljoin(self._open_api, "datasets")
        return get(url, params=params, access_key=self.access_key, content_type=JSON_CONTENT_TYPE)


T = TypeVar("T")  # pylint: disable=invalid-name


def multithread_upload(
    function: Callable[[T], None],
    arguments: Iterable[T],
    *,
    jobs: int = 1,
) -> None:
    """multi-thread upload framework

    :param function: The upload function
    :param arguments: The arguments of the upload function
    :param jobs: The number of the max workers in multithread upload
    """
    with ThreadPoolExecutor(jobs) as executor:
        futures = []
        for argument in arguments:
            futures.append(executor.submit(function, argument))

        done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
        for future in not_done:
            future.cancel()
        for future in done:
            future.result()


def post(
    url: str,
    *,
    data: Optional[bytes] = None,
    json_data: Optional[Dict[str, Any]] = None,
    content_type: Optional[str] = None,
    max_retries: Optional[int] = None,
    timeout: Optional[int] = None,
    access_key: Optional[str] = None,
) -> Any:
    """Send a POST requests

    :param url: URL for the request
    :param data: bytes data to send in the body of the request
    :param json_data: json data to send in the body of the request
    :param content_type: Content-Type to send in the header of the request
    :param max_retries: max_retries to send in the header of the request
    :param timeout: timeout to send in the header of the request
    :param access_key: user's access key
    :raises GASRequestError: When post request failed
    :return: response of the request
    """

    if not max_retries:
        max_retries = default_config.max_retries
    if not timeout:
        timeout = default_config.timeout

    headers: Dict[str, str] = {}
    if access_key:
        headers["X-Token"] = access_key
    if content_type:
        headers["Content-Type"] = content_type

    for i in range(max_retries):
        try:
            response = requests.post(
                url, data=data, json=json_data, headers=headers, timeout=timeout
            )
            return _parser_response(response)
        except (requests.RequestException, GASResponseError) as error:
            if i == max_retries - 1:
                raise error
            logger.warning(error)
            logger.warning("retrying: %d/%d", i + 1, max_retries)
            time.sleep(3)


def get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    content_type: Optional[str] = None,
    access_key: Optional[str] = None,
) -> Any:
    """Send a GET requests

    :param url: URL for the request
    :param params: Dictionary to send in the query string for the `Request`
    :param content_type: Content-Type to send in the header of the request
    :param access_key: user's access key
    :raises GASRequestError: When post request failed
    :return: response of the request
    """

    headers: Dict[str, str] = {}
    if access_key:
        headers["X-Token"] = access_key
    if content_type:
        headers["Content-Type"] = content_type

    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.RequestException as error:
        raise GASRequestError(error) from error

    return _parser_response(response)


def _parser_response(response: requests.Response) -> Any:
    if response.status_code not in (200, 201):
        raise GASResponseError(response)
    return response
