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
"""rptk module.format.test module."""

from __future__ import print_function
from __future__ import unicode_literals

from rptk.format import BaseFormat


class TestFormat(BaseFormat):
    """Returns result object as a python dict object."""

    description = "Test output format"

    def format(self, result=None, name=None):
        """Construct and return output dict."""
        self.log_method_enter(method=self.current_method)
        name = super(TestFormat, self).format(result=result, name=name)
        output = {
            name: result
        }
        self.log_method_exit(method=self.current_method)
        return output

    def validate(self, output=None):
        """Validate output dict object."""
        self.log_method_enter(method=self.current_method)
        if not isinstance(output, dict):
            self.raise_type_error(arg=output, cls=dict)
        self.log_method_exit(method=self.current_method)
        return True
