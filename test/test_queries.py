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
"""rptk query class test cases."""

from __future__ import print_function
from __future__ import unicode_literals

import importlib

from helpers import available_policies, default_query_classes, objects

import pytest


class TestQueryClass(object):
    """Test cases for rptk query classes."""

    @pytest.mark.parametrize("path", default_query_classes().values())
    @pytest.mark.parametrize("policy", available_policies().keys())
    @pytest.mark.parametrize("objects", objects())
    def test_query_class(self, posix, path, policy, objects, validate_schema):
        """Test rptk query class."""
        mod_path, cls_name = path.rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, cls_name)
        with cls(host="whois.radb.net", port=43, policy=policy) as q:
            if q.posix_only and not posix:
                pytest.skip("skipping posix only test")
            result = q.query(*objects)
        assert validate_schema(result, "get_prefix_list.schema")
