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

import ipaddress
import json
import os

import jsonschema

import pytest

import yaml

from rptk.web import app


@pytest.fixture(scope="module")
def client():
    """Get test http client."""
    return app.test_client


@pytest.fixture(scope="session")  # noqa: C901
def format_checker():
    """Get a custom format_checker instance."""
    format_checker = jsonschema.FormatChecker()

    def coerce_to_unicode(value):
        try:
            value = unicode(value)
        except (ValueError, NameError):
            pass
        return value

    @format_checker.checks("ipv4-prefix", raises=ValueError)
    def is_ipv4_prefix(instance):
        instance = coerce_to_unicode(instance)
        try:
            ipaddress.IPv4Network(instance, strict=True)
            return True
        except Exception:
            return False

    @format_checker.checks("ipv6-prefix", raises=ValueError)
    def is_ipv6_prefix(instance):
        instance = coerce_to_unicode(instance)
        try:
            ipaddress.IPv6Network(instance, strict=True)
            return True
        except Exception:
            return False

    @format_checker.checks("ipv4-address-prefix", raises=ValueError)
    def is_ipv4_address_prefix(instance):
        instance = coerce_to_unicode(instance)
        try:
            ipaddress.IPv4Network(instance, strict=False)
            return True
        except Exception:
            return False

    @format_checker.checks("ipv6-address-prefix", raises=ValueError)
    def is_ipv6_address_prefix(instance):
        instance = coerce_to_unicode(instance)
        try:
            ipaddress.IPv6Network(instance, strict=False)
            return True
        except Exception:
            return False

    return format_checker


@pytest.fixture(scope="session")
def validate_schema(format_checker):
    """Return a callable that will validate data against a schema."""
    def _validate(data, schema_file):
        schema_dir = os.path.join(os.path.dirname(__file__), "schemas")
        with open(os.path.join(schema_dir, schema_file)) as f:
            schema = json.load(f)
        jsonschema.validate(instance=data, schema=schema,
                            format_checker=format_checker)
        return True
    return _validate


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

    @pytest.mark.parametrize("format",
                             ("junos", "ios", "ios_null", "plain", "bird"))
    def test_get_prefix_list_other(self, client, validate_schema, format):
        """Test get_prefix_list method."""
        uri = "/{}/{}".format(format, self.obj)
        with client() as c:
            resp = c.get(uri)
        assert resp.status_code == 200
        assert resp.content_type == "text/plain"
        assert resp.data
