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
"""rptk format class test cases."""

from __future__ import print_function
from __future__ import unicode_literals

import importlib
import json
import os

from helpers import default_format_classes, objects

import pytest

import yaml


class TestFormatClass(object):
    """Test cases for rptk format classes."""

    data_dir = os.path.join(os.path.dirname(__file__), "data")

    @pytest.mark.parametrize(("format", "path"),
                             default_format_classes().items())
    @pytest.mark.parametrize("objects", objects())
    def test_format_class(self, format, path, objects, validate_schema):
        """Test rptk format class."""
        mod_path, cls_name = path.rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, cls_name)
        result = dict()
        for obj in objects:
            with open(os.path.join(self.data_dir, "{}.json".format(obj))) as f:
                result.update(json.load(f))
        with cls() as f:
            output = f.format(result=result)
        if format == "json":
            assert validate_schema(json.loads(output),
                                   "get_prefix_list.schema")
        elif format == "yaml":
            assert validate_schema(yaml.load(output),
                                   "get_prefix_list.schema")
        else:
            for obj in objects:
                assert obj in output
