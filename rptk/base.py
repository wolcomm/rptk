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
"""rptk base module."""

from __future__ import print_function
from __future__ import unicode_literals

import inspect
import logging


class BaseObject(object):
    """BaseObject class providing generic logging functionality."""

    def __init__(self):
        """Initialise object."""
        self._log = logging.getLogger(self.__module__)

    def __repr__(self):
        """Provide generic string representation."""
        return "%s() object" % self.cls_name

    def __enter__(self):
        """Log context manager entry."""
        self.log_ready_start()
        self.log_ready_done()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log context manager exit."""
        self.log_exit_start()
        self.log_exit_done()

    @property
    def opts(self):
        """Get self.opts if it exists."""
        return getattr(self, "_opts", None)

    @property
    def log(self):
        """Get the current logger."""
        return self._log

    @property
    def cls_name(self):
        """Get the class name of self."""
        return self.__class__.__name__

    @property
    def current_method(self):
        """Get the currently executing method name."""
        return inspect.currentframe().f_back.f_code.co_name

    def log_init(self):
        """Log entry into the __init__ method."""
        self.log.debug(msg="initialising %s instance" % self.cls_name)

    def log_init_done(self):
        """Log exit from an __init__ method."""
        caller = inspect.currentframe().f_back.f_back.f_code.co_name
        if caller == '__init__':
            self.log.debug(msg="still initialising %s instance" % self.cls_name)  # noqa: E501
        else:
            self.log.debug(msg="%s instance initialised" % self.cls_name)

    def log_method_enter(self, method=None):
        """Log entry into a class method."""
        self.log.debug(msg="entering method %s.%s" % (self.cls_name, method))

    def log_method_exit(self, method=None):
        """Log exit from a class method."""
        self.log.debug(msg="leaving method %s.%s" % (self.cls_name, method))

    def log_ready_start(self):
        """Log start of object initialisation."""
        self.log.debug(msg="preparing %s for use" % self)

    def log_ready_done(self):
        """Log end of object initialisation."""
        self.log.debug(msg="%s ready for use" % self)

    def log_exit_start(self):
        """Log start of object cleanup."""
        self.log.debug(msg="cleaning up %s" % self)

    def log_exit_done(self):
        """Log end of object cleanup."""
        self.log.debug(msg="finished cleaning up %s" % self)

    def raise_type_error(self, arg=None, cls=None):
        """Raise a TypeError with useful logging."""
        msg = "argument %s (%s) not of type %s" % (
            arg.__name__, arg, cls
            )
        self.log.error(msg=msg)
        raise TypeError(msg)

    def raise_runtime_error(self, msg=None):
        """Raise a RuntimeError with useful logging."""
        self.log.error(msg=msg)
        raise RuntimeError(msg)
