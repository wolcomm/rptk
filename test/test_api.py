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

import itertools
import os

import pytest

from rptk import RptkAPI


@pytest.fixture(scope="session")
def api():
    """Construct an API instance with the test config."""
    config_file = os.path.join(os.path.dirname(__file__), 'tests.conf')
    return RptkAPI(config_file=config_file)


@pytest.fixture(scope="session")
def posix():
    """Check whether we are on a POSIX system."""
    return os.name == "posix"


def classmap(api):
    """Construct a cartesian product of the available classes."""
    return itertools.product(api.query_class_loader.class_names,
                             api.format_class_loader.class_names)


class TestAPI(object):
    """Test cases for rptk python API."""

    @pytest.mark.parametrize(("q", "f"), classmap(api()))
    def test_api(self, api, posix, q, f):
        """Test rptk python API."""
        if api.query_class_loader.get_class(name=q).posix_only and not posix:
            pytest.skip("skipping posix only test")
        api.update(query_class_name=q, format_class_name=f)
        result = api.query(test=True)
        assert result
