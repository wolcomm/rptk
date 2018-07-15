# Copyright (c) 2018 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License version 2.0
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rptk web-api test cases."""

from __future__ import print_function
from __future__ import unicode_literals

import re

from helpers import default_format_classes, objects

import pytest

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


server_re = re.compile(r"^rptk-web/\d+.\d+.\d(-\w+\.\d+)?$")


@pytest.mark.usefixtures("mock_query_classes")
class TestWebAPI(object):
    """Test cases for rptk web API."""

    def test_get_formats(self, client, validate_schema):
        """Test get_formats method."""
        uri = "/formats"
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        assert server_re.match(resp.headers["Server"])
        data = resp.json
        assert validate_schema(data, "get_formats.schema")

    def test_get_policies(self, client, validate_schema):
        """Test get_policies method."""
        uri = "/policies"
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        assert server_re.match(resp.headers["Server"])
        data = resp.json
        assert validate_schema(data, "get_policies.schema")

    @pytest.mark.parametrize("f", default_format_classes().keys())
    @pytest.mark.parametrize("objects", objects())
    def test_get_prefix_list(self, client, validate_schema, f, objects):
        """Test get_prefix_list method."""
        base_uris = [
            "/query?format={}".format(f),
            "/{}/query?".format(f)
        ]
        uris = list()
        for uri in base_uris:
            for obj in objects:
                uri += "&objects={}".format(obj)
            uris.append(uri)
        if len(objects) == 1:
            uris.append("/{}/{}".format(f, objects[0]))
        print("uris: {}".format(uris))
        for uri in uris:
            with client() as c:
                resp = c.get(uri)
            assert resp.status_code == 200
            assert server_re.match(resp.headers["Server"])
            if f == "json":
                assert resp.content_type == "application/json"
                data = resp.json
                assert validate_schema(data, "get_prefix_list.schema")
            elif f == "yaml":
                assert resp.content_type == "application/x-yaml"
                data = yaml.load(resp.data, Loader=Loader)
                assert validate_schema(data, "get_prefix_list.schema")
            else:
                assert resp.content_type == "text/plain"
                for obj in objects:
                    assert obj in resp.data.decode()
