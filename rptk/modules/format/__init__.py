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

import datetime

import jinja2

from rptk.base import BaseObject


class BaseFormat(BaseObject):
    """Base class for the definition of output format classes."""

    description = None

    def __init__(self, **opts):
        """Initialise new object."""
        super(BaseFormat, self).__init__()
        self.log_init()
        self._opts = opts
        self.log_init_done()

    def format(self, result=None, name=None):
        """Check the result type and name."""
        self.log_method_enter(method=self.current_method)
        if not isinstance(result, dict):
            self.raise_type_error(arg=result, cls=dict)
        if not name:
            self.log.debug(msg="using name from configuration")
            name = self.name
        if not isinstance(name, basestring):
            self.raise_type_error(arg=name, cls=basestring)
        output = unicode(name)
        self.log_method_exit(method=self.current_method)
        return output

    def validate(self, output=None):
        """Check that output is a valid string type."""
        self.log_method_enter(method=self.current_method)
        if not isinstance(output, basestring):
            self.raise_type_error(arg=output, cls=basestring)
        self.log.debug(msg="validation successful")
        self.log_method_exit(method=self.current_method)
        return True

    @property
    def name(self):
        """Get output name."""
        return self.opts["name"]


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
            self.raise_runtime_error(e.message)
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
            self.log.error(msg=e.message)
            raise
        self.log.debug("template loaded successfully")

    def format(self, result=None, name=None):
        """Render output from template."""
        self.log_method_enter(method=self.current_method)
        name = super(JinjaFormat, self).format(result=result, name=name)
        if isinstance(self.template, jinja2.Template):
            try:
                output = self.template.render(result=result, name=name,
                                              now=datetime.datetime.now())
                self.log_method_exit(method=self.current_method)
                return output
            except Exception as e:
                self.log.error(msg=e.message)
                raise
        else:
            self.raise_type_error(arg=self.template, cls=jinja2.Template)
