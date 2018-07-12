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
"""rptk module.format module."""

from __future__ import print_function
from __future__ import unicode_literals

import datetime

import jinja2

from rptk.base import BaseObject


try:
    basestring
except NameError:
    basestring = str


try:
    unicode
except NameError:
    unicode = str


class BaseFormat(BaseObject):
    """Base class for the definition of output format classes."""

    description = None
    content_type = "text/plain"

    def __init__(self, **opts):
        """Initialise new object."""
        super(BaseFormat, self).__init__()
        self.log_init()
        self._opts = opts
        self.log_init_done()

    def format(self, result=None):
        """Check the result type and name."""
        self.log_method_enter(method=self.current_method)
        if not isinstance(result, dict):
            self.raise_type_error(arg=result, cls=dict)
        self.log_method_exit(method=self.current_method)


class JinjaFormat(BaseFormat):
    """Base class for Jinja2 template-based output format classes."""

    template_name = None

    def __init__(self, **opts):
        """Initialise new object."""
        super(JinjaFormat, self).__init__(**opts)
        self.log.debug("configuring jinja2 environment")
        try:
            self.env = jinja2.Environment(
                loader=jinja2.PackageLoader('rptk')
            )
            self.env.trim_blocks = True
            self.env.lstrip_blocks = True
        except Exception as e:
            self.raise_runtime_error("{}".format(e))
        self._template = None
        self.log_init_done()

    def __enter__(self):
        """Load Jinja2 template."""
        self.log_ready_start()
        self._load_template()
        self.log_ready_done()
        return self

    @property
    def template(self):
        """Get loaded Jinja2 template object."""
        return self._template

    def _load_template(self):
        """Load template into Jinja2 Environment instance."""
        try:
            self._template = self.env.get_template(self.template_name)
        except jinja2.TemplateError as e:
            self.log.error(msg="{}".format(e))
            raise
        self.log.debug("template loaded successfully")

    def format(self, result=None):
        """Render output from template."""
        self.log_method_enter(method=self.current_method)
        super(self.__class__, self).format(result=result)
        if isinstance(self.template, jinja2.Template):
            try:
                output = self.template.render(result=result,
                                              now=datetime.datetime.now())
            except Exception as e:
                self.log.error(msg="{}".format(e))
                raise
        else:
            self.raise_type_error(arg=self.template, cls=jinja2.Template)
        self.log_method_exit(method=self.current_method)
        return output
