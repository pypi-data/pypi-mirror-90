# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json


class _StdoutStream(object):
    def __call__(self, chunk):
        print(chunk)


def response_content(response, streamed, action, chunk_size):
    if streamed is False:
        return response.content

    if action is None:
        action = _StdoutStream()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            action(chunk)


def decode_response(response):
    """
    :returns:
        Decoded JSON content as a dict, or raw text if content could not be
        decoded as JSON.
    :raises:
        requests.HTTPError if the response contains an HTTP error status code.
    """
    content_type = response.headers.get("content-type", "")

    content = response.content.strip()
    if response.encoding:
        content = content.decode(response.encoding)
    if not content:
        return content
    if content_type.split(";")[0] != "application/json":
        return content
    try:
        return json.loads(content)
    except ValueError:
        raise ValueError("Invalid json content: {}".format(content))
