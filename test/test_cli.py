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

from helpers import (default_query_classes,
                     default_format_classes,
                     available_policies,
                     objects)

import pytest

query_args = [None] + ["--query={}".format(q)
                       for q in default_query_classes().keys()]

format_args = [None] + ["--format={}".format(f)
                        for f in default_format_classes().keys()]

policy_args = [None] + ["--policy={}".format(p)
                        for p in available_policies().keys()]


@pytest.mark.usefixtures("mock_query_classes")
class TestCLI(object):
    """Test cases for rptk command-line tool."""

    @pytest.mark.parametrize("q", query_args)
    @pytest.mark.parametrize("f", format_args)
    @pytest.mark.parametrize("p", policy_args)
    @pytest.mark.parametrize("obj", objects())
    def test_cli(self, capsys, cli_entry_point, q, f, p, obj):
        """Test rptk command-line tool."""
        sys.argv[0] = "rptk"
        argv = [arg for arg in (q, f, p, obj) if arg is not None]
        try:
            cli_entry_point(argv=argv)
        except SystemExit as exit:
            captured = capsys.readouterr()
            assert exit.code == 0
            assert "AS37271" in captured.out
