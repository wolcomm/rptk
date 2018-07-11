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

from helpers import default_query_classes, default_format_classes

import pytest


class TestAPI(object):
    """Test cases for rptk python API."""

    @pytest.mark.parametrize("q", default_query_classes().keys())
    @pytest.mark.parametrize("f", default_format_classes().keys())
    def test_api(self, api, posix, q, f):
        """Test rptk python API."""
        if api.query_class_loader.get_class(name=q).posix_only and not posix:
            pytest.skip("skipping posix only test")
        api.update(query_class_name=q, format_class_name=f)
        result = api.query()
        assert result
