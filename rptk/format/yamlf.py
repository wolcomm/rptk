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
"""rptk module.format.yamlf module."""

from __future__ import print_function
from __future__ import unicode_literals

import yaml

from rptk.format import BaseFormat


class YamlFormat(BaseFormat):
    """Renders result object as a YAML document."""

    description = "YAML object representation"
    content_type = "application/x-yaml"

    def format(self, result=None, name=None):
        """Render output as YAML."""
        self.log_method_enter(method=self.current_method)
        name = super(YamlFormat, self).format(result=result, name=name)
        self.log.debug(msg="creating json output")
        try:
            output = yaml.dump(
                {name: result},
                indent=4,
                explicit_start=True,
                explicit_end=True,
                default_flow_style=False,
            )
            self.log_method_exit(method=self.current_method)
            return output
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise

    def validate(self, output=None):
        """Validate JSON document."""
        self.log_method_enter(method=self.current_method)
        super(YamlFormat, self).validate(output=output)
        try:
            yaml.load(output)
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise
        self.log_method_exit(method=self.current_method)
        return True
