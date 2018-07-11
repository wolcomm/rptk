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
"""Fixtures for rptk test cases."""

from __future__ import print_function
from __future__ import unicode_literals

import importlib
import ipaddress
import json
import os

import jsonschema

from pkg_resources import load_entry_point

import pytest


@pytest.fixture
def mock_query_classes(monkeypatch):
    """Monkeypatch query classes for testing."""
    from rptk import RptkAPI
    from rptk.query import BaseQuery

    class _MockQuery(BaseQuery):
        def query(self, obj=None):
            obj = super(self.__class__, self).query(obj=obj)
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            with open(os.path.join(data_dir, "{}.json".format(obj))) as f:
                result = json.load(f)
            return result

    for path in RptkAPI.default_query_classes.values():
        mod_path, cls_name = path.rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        monkeypatch.setattr(mod, cls_name, _MockQuery)


@pytest.fixture(scope="module")
def cli_entry_point():
    """Get the entry point function for the rptk command-line tool."""
    return load_entry_point(dist="rptk", group="console_scripts", name="rptk")


@pytest.fixture(scope="module")
def client():
    """Get test http client."""
    from rptk.web import app
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


@pytest.fixture(scope="session")
def api():
    """Construct an API instance with the test config."""
    from rptk import RptkAPI
    config_file = os.path.join(os.path.dirname(__file__), 'tests.conf')
    return RptkAPI(config_file=config_file)


@pytest.fixture(scope="session")
def posix():
    """Check whether we are on a POSIX system."""
    return os.name == "posix"
