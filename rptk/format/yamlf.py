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

import logging

from rptk.format import BaseFormat

import yaml

try:
    from yaml import CDumper as Dumper
except ImportError as e:
    logging.getLogger(__name__).warning("%s: falling back to python dumper", e)
    from yaml import Dumper


class YamlFormat(BaseFormat):
    """Renders result object as a YAML document."""

    description = "YAML object representation"
    content_type = "application/x-yaml"

    def format(self, result=None):
        """Render output as YAML."""
        self.log_method_enter(method=self.current_method)
        super(self.__class__, self).format(result=result)
        self.log.debug(msg="creating json output")
        try:
            output = yaml.dump(result, Dumper=Dumper, indent=4,
                               explicit_start=True, explicit_end=True,
                               default_flow_style=False)
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log_method_exit(method=self.current_method)
        return output
