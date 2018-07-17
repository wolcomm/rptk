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
"""rptk module.query.native.exceptions module."""

from __future__ import print_function
from __future__ import unicode_literals


class IRRQueryError(RuntimeError):
    """Exception raised during query execution."""

    proto_msg = ''

    def __init__(self, *args, **kwargs):
        """Initialise the Exception instance."""
        super(IRRQueryError, self).__init__(self.proto_msg, *args, **kwargs)


class KeyNotFoundError(IRRQueryError):
    """The RPSL key was not found."""

    proto_msg = "Key not found. (D)"


class KeyNotUniqueError(IRRQueryError):
    """There are multiple copies of the key in one database. (E)."""

    proto_msg = "There are multiple copies of the key in one database. (E)"


class OtherError(IRRQueryError):
    """An unknown error occured during query execution."""

    proto_msg = "Some other error, see the <optional message> for details."
