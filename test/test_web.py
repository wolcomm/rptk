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

from helpers import default_format_classes as formats
from helpers import objects

import pytest

import yaml

text_formats = (f for f in formats().keys() if f not in ("json", "yaml"))


@pytest.mark.usefixtures("mock_query_classes")
class TestWebAPI(object):
    """Test cases for rptk web API."""

    obj = "AS37271"

    def test_get_formats(self, client, validate_schema):
        """Test get_formats method."""
        uri = "/formats"
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        data = resp.json
        assert validate_schema(data, "get_formats.schema")

    def test_get_policies(self, client, validate_schema):
        """Test get_policies method."""
        uri = "/policies"
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        data = resp.json
        assert validate_schema(data, "get_policies.schema")

    def test_get_prefix_list_json(self, client, validate_schema):
        """Test get_prefix_list method with json output."""
        uri = "/json/{}".format(self.obj)
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        data = resp.json
        assert validate_schema(data, "get_prefix_list.schema")

    def test_get_prefix_list_yaml(self, client, validate_schema):
        """Test get_prefix_list method with yaml output."""
        uri = "/yaml/{}".format(self.obj)
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "application/x-yaml"
        data = yaml.load(resp.data)
        assert validate_schema(data, "get_prefix_list.schema")

    @pytest.mark.parametrize("f", text_formats)
    @pytest.mark.parametrize("objects", objects())
    def test_get_prefix_list_text(self, client, validate_schema, f, objects):
        """Test get_prefix_list method."""
        if len(objects) == 1:
            uri = "/{}/{}".format(f, self.obj)
        else:
            pytest.xfail()
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "text/plain"
        assert resp.data
