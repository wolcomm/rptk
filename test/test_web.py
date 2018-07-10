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
def validate_resp(format_checker):
    """Return a callable that will validate response data against a schema."""
    def _validate(resp, schema_file):
        schema_dir = os.path.join(os.path.dirname(__file__), "schemas")
        with open(os.path.join(schema_dir, schema_file)) as f:
            schema = json.load(f)
        jsonschema.validate(instance=resp.json, schema=schema,
                            format_checker=format_checker)
        return True
    return _validate


class TestWebAPI(object):
    """Test cases for rptk web API."""

    def test_get_formats(self, client, validate_resp):
        """Test get_formats method."""
        with client() as c:
            resp = c.get("/formats")
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        assert validate_resp(resp, "get_formats.schema")

    def test_get_policies(self, client, validate_resp):
        """Test get_policies method."""
        with client() as c:
            resp = c.get("/policies")
        assert resp.status_code == 200
        assert resp.content_type == "application/json"
        assert validate_resp(resp, "get_policies.schema")
