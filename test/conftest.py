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
import json
import os

import pytest


@pytest.fixture
def mock_query_classes(monkeypatch):
    """Monkeypatch query classes for testing."""
    from rptk import RptkAPI
    from rptk.query import BaseQuery

    class _MockQuery(BaseQuery):
        def query(self, obj=None):
            print("self: {}, cls: {}".format(self, self.__class__))
            obj = super(self.__class__, self).query(obj=obj)
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            with open(os.path.join(data_dir, "{}.json".format(obj))) as f:
                result = json.load(f)
            return result

    for path in RptkAPI.default_query_classes.values():
        mod_path, cls_name = path.rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        monkeypatch.setattr(mod, cls_name, _MockQuery)
