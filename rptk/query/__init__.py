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
"""rptk module.query module."""

from __future__ import print_function
from __future__ import unicode_literals

from rptk.base import BaseObject


try:
    basestring
except NameError:
    basestring = str


try:
    unicode
except NameError:
    unicode = str


class BaseQuery(BaseObject):
    """Base class for the definition of query execution classes."""

    posix_only = False

    def __init__(self, **opts):
        """Initialise new object."""
        super(BaseQuery, self).__init__()
        self.log_init()
        self._opts = opts
        self.log_init_done()

    def query(self, *objects):
        """Check the object name type."""
        self.log_method_enter(method=self.current_method)
        for obj in objects:
            if not isinstance(obj, basestring):
                self.raise_type_error(arg=obj, cls=basestring)
            obj = unicode(obj)
            yield obj

    @property
    def host(self):
        """Get the configured IRR server hostname."""
        return self.opts["host"]

    @property
    def port(self):
        """Get the configured IRR server port."""
        return int(self.opts["port"])

    @property
    def target(self):
        """Construct a hostname:port pair for the IRR server."""
        return "{}:{}".format(self.host, self.port)
