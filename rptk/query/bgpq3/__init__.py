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
"""rptk module.query.bgpq3 module."""

from __future__ import print_function
from __future__ import unicode_literals


try:
    from rptk.query.bgpq3._async import _Bgpq3QueryAsync as Bgpq3Query  # noqa: F401, E501
except (ImportError, SyntaxError):
    from rptk.query.bgpq3._sync import _Bgpq3QuerySync as Bgpq3Query  # noqa: F401, E501
