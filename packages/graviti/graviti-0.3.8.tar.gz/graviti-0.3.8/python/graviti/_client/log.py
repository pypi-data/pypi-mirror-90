# !/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""logging utility functions for dumping http request and response"""

import json
from typing import MutableMapping

from requests.models import PreparedRequest, Response
from requests_toolbelt.multipart.encoder import FileWrapper, MultipartEncoder

REQUEST_TEMPLATE = """
===================================================================
########################## HTTP Request ###########################
"url": {}
"method": {}
"headers": {}
"body": {}
"""

RESPONSE_TEMPLATE = """
########################## HTTP Response ##########################
"url": {}
"status_code": {}
"reason": {}
"headers": {}
"content": {}
===================================================================
"""


def dump_request_and_response(response: Response) -> str:
    """dump http request and response

    :param response: http response and response
    :return: string of http request and response for logging, example:
    ===================================================================
    ########################## HTTP Request ###########################
    "url": https://gas.graviti.cn/gatewayv2/content-store/putObject
    "method": POST
    "headers": {
      "User-Agent": "python-requests/2.23.0",
      "Accept-Encoding": "gzip, deflate",
      "Accept": "*/*",
      "Connection": "keep-alive",
      "X-Token": "c3b1808b21024eb38f066809431e5bb9",
      "Content-Type": "multipart/form-data; boundary=5adff1fc0524465593d6a9ad68aad7f9",
      "Content-Length": "330001"
    }
    "body":
    --5adff1fc0524465593d6a9ad68aad7f9
    b'Content-Disposition: form-data; name="contentSetId"\r\n\r\n'
    b'e6110ff1-9e7c-4c98-aaf9-5e35522969b9'

    --5adff1fc0524465593d6a9ad68aad7f9
    b'Content-Disposition: form-data; name="filePath"\r\n\r\n'
    b'4.jpg'

    --5adff1fc0524465593d6a9ad68aad7f9
    b'Content-Disposition: form-data; name="fileData"; filename="4.jpg"\r\n\r\n'
    [329633 bytes of object data]

    --5adff1fc0524465593d6a9ad68aad7f9--

    ########################## HTTP Response ###########
    "url": https://gas.graviti.cn/gatewayv2/content-stor
    "status_code": 200
    "reason": OK
    "headers": {
      "Date": "Sat, 23 May 2020 13:05:09 GMT",
      "Content-Type": "application/json;charset=utf-8",
      "Content-Length": "69",
      "Connection": "keep-alive",
      "Access-Control-Allow-Origin": "*",
      "X-Kong-Upstream-Latency": "180",
      "X-Kong-Proxy-Latency": "112",
      "Via": "kong/2.0.4"
    }
    "content": {
      "success": true,
      "code": "DATACENTER-0",
      "message": "success",
      "data": {}
    }
    ====================================================
    """
    return _dump_request(response.request) + _dump_response(response)


def _dump_request(request: PreparedRequest) -> str:
    """dump http request

    :param request: http request
    :return: string of http request for logging
    """
    headers = _dump_headers(request.headers)
    body = "N/A"
    content_type = request.headers.get("Content-Type", None)
    if content_type:
        if content_type.startswith("multipart/form-data"):
            body = _dump_multipart_encoder(request.body)
        elif isinstance(request.body, bytes):
            body = request.body.decode("unicode_escape")

    return REQUEST_TEMPLATE.format(request.url, request.method, headers, body)


def _dump_response(response: Response) -> str:
    """dump http response

    :param response: http response
    :return: string of http response for logging
    """
    headers = _dump_headers(response.headers)
    content = "N/A"

    content_type = response.headers.get("Content-Type", None)
    if content_type:
        if content_type.startswith("application/json"):
            content = json.dumps(response.json(), indent=2)
        elif content_type.startswith("text"):
            content = response.text
        elif len(response.content) > 512:
            content = f"[{len(response.content)} bytes of object data]"
        else:
            content = str(response.content)

    return RESPONSE_TEMPLATE.format(
        response.url, response.status_code, response.reason, headers, content
    )


def _dump_multipart_encoder(body: MultipartEncoder) -> str:
    """dump MultipartEncoder multipart/form-data Content-Type post_data

    :param body: MultipartEncoder multipart/formdata post data
    :return: string of multipart/form-data post data for logging
    """
    lines = []
    boundary = body.boundary
    for part in body.parts:
        lines.append("\n" + boundary)
        lines.append(str(part.headers))
        body = part.body
        if isinstance(body, FileWrapper):
            if body.fd.closed:
                lines.append("[file closed]")
            else:
                lines.append(f"[{body.fd.tell()} bytes of object data]")
        else:
            lines.append(str(body.getvalue()))

    lines.append("\n" + boundary + "--")

    return "\n".join(lines)


def _dump_headers(headers: MutableMapping[str, str]) -> str:
    """dump http headers as json format string for logging

    :param headers: headers of http request or response
    :return: json format string of headers content
    """
    return json.dumps(dict(headers), indent=2)
