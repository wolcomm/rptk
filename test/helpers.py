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
"""Helper functions and constants for rptk test cases."""

from __future__ import print_function
from __future__ import unicode_literals

from rptk import RptkAPI


def objects():
    """Return a tuple of RPSL objects to test against."""
    return ("AS37271", "AS37271:AS-CUSTOMERS")


def default_query_classes():
    """Return the dict of default query classes to test with."""
    return RptkAPI.default_query_classes


def default_format_classes():
    """Return the dict of default format classes to test with."""
    return RptkAPI.default_format_classes


def available_policies():
    """Return the dict of available resolution policies to test with."""
    return RptkAPI.available_policies
