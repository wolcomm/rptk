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
"""rptk CLI test cases."""

from __future__ import print_function
from __future__ import unicode_literals

import sys

from helpers import (objects)

import pytest

args = (
    # ["--debug"],
    [],
    ["--policy=strict", "--query=bgpq3", "--format=yaml"]
)


@pytest.mark.usefixtures("mock_query_classes")
class TestCLI(object):
    """Test cases for rptk command-line tool."""

    @pytest.mark.parametrize("args", args)
    @pytest.mark.parametrize("objects", objects())
    def test_cli(self, capsys, cli_entry_point, args, objects):
        """Test rptk command-line tool."""
        sys.argv[0] = "rptk"
        argv = args + list(objects)
        try:
            cli_entry_point(argv=argv)
        except SystemExit as exit:
            captured = capsys.readouterr()
            assert exit.code == 0
            for obj in objects:
                assert obj in captured.out
