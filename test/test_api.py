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
"""rptk API test cases."""

from __future__ import print_function
from __future__ import unicode_literals

from helpers import (available_policies, default_format_classes,
                     default_query_classes, objects)

import pytest


@pytest.mark.usefixtures("mock_query_classes")
class TestAPI(object):
    """Test cases for rptk python API."""

    @pytest.mark.parametrize("q", default_query_classes().keys())
    @pytest.mark.parametrize("f", default_format_classes().keys())
    @pytest.mark.parametrize("p", available_policies().keys())
    @pytest.mark.parametrize("obj", objects())
    def test_api(self, q, f, p, obj):
        """Test rptk python API."""
        from rptk import RptkAPI
        with RptkAPI(query_class_name=q, format_class_name=f,
                     query_policy=p) as api:
            result = api.query(obj)
            output = api.format(result=result)
        assert output
