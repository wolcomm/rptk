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
"""rptk API module."""

from __future__ import print_function
from __future__ import unicode_literals

from rptk import dispatch


class Rptk(object):
    """rptk API class."""

    def __init__(self, **opts):
        """Initialise API object."""
        self._dispatcher = dispatch.Dispatcher(**opts)

    def query(self, obj=None, name=None, test=False):
        """Perform query."""
        return self._dispatcher.dispatch(obj=obj, name=name, test=test)

    def available_formats(self):
        """Get list of available formats."""
        return self._dispatcher.format_class_loader.class_info

    def available_policies(self):
        """Get list of available resolution policies."""
        return ('strict', 'loose',)

    def update_opts(self, **opts):
        """Update API options from keyword args."""
        try:
            self._dispatcher.update(**opts)
        except Exception as e:
            raise e
        return self

    @property
    def query_class_loader(self):
        """Get the query class loader object."""
        return self._dispatcher.query_class_loader

    @property
    def format_class_loader(self):
        """Get the format class loader object."""
        return self._dispatcher.format_class_loader

    @property
    def opts(self):
        """Get the current options."""
        return self._dispatcher.opts

    def __getattribute__(self, name):
        """Return value from self.opts dict."""
        try:
            return super(Rptk, self).__getattribute__(name)
        except AttributeError as e:
            try:
                return self.opts[name]
            except KeyError:
                pass
            raise e

    def __setattr__(self, name, value):
        """Set value on Dispatcher object."""
        try:
            self._dispatcher.update(**{name: value})
        except Exception:
            super(Rptk, self).__setattr__(name, value)
