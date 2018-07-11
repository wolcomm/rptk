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

from pkg_resources import load_entry_point

import pytest


query_args = (
    None,
    "--query=native",
    "--query=bgpq3"
)

format_args = (
    None,
    "--format=junos",
    "--format=yaml",
    "--format=json",
    "--format=ios",
    "--format=ios_null",
    "--format=plain",
    "--format=bird"
)

policy_args = (
    None,
    "--policy=loose",
    "--policy=strict",
)

object_args = (
    "AS37271",
    "AS37271:AS-CUSTOMERS"
)


@pytest.fixture(scope="module")
def main():
    """Get the entry point function for the rptk command-line tool."""
    return load_entry_point(dist="rptk", group="console_scripts", name="rptk")


@pytest.mark.usefixtures("mock_query_classes")
class TestCLI(object):
    """Test cases for rptk command-line tool."""

    @pytest.mark.parametrize("q", query_args)
    @pytest.mark.parametrize("f", format_args)
    @pytest.mark.parametrize("p", policy_args)
    @pytest.mark.parametrize("obj", object_args)
    def test_cli(self, capsys, main, q, f, p, obj):
        """Test rptk command-line tool."""
        sys.argv[0] = "rptk"
        argv = [arg for arg in (q, f, p, obj) if arg is not None]
        try:
            main(argv=argv)
        except SystemExit as exit:
            captured = capsys.readouterr()
            assert exit.code == 0
            assert "AS37271" in captured.out
