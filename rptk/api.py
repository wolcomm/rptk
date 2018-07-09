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

import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import sys

from rptk.base import BaseObject
from rptk.load import ClassLoader


class Rptk(BaseObject):
    """rptk API class."""

    def __init__(self, config_file=None, **kwargs):
        """Initialise API object."""
        super(self.__class__, self).__init__()
        self.log_init()
        self.log.debug(msg="creating options namespaces")
        self._options = {
            "query_": argparse.Namespace(),
            "format_": argparse.Namespace()
        }
        self.log.debug(msg="determining config file location")
        self._config_file = config_file or self._find_config_file()
        self.log.debug(msg="reading config file at {}"
                           .format(self.config_file))
        reader = self._read_config()
        self.log.debug(msg="setting configuration file options")
        for key, value in reader.items("query"):
            self.log.debug(msg="setting query_{} = {}".format(key, value))
            setattr(self.query_options, key, value)
        for key, value in reader.items("format"):
            self.log.debug(msg="setting format_{} = {}".format(key, value))
            setattr(self.format_options, key, value)
        self.log.debug(msg="updating options with user supplied values")
        self.update(**kwargs)
        self.log.debug(msg="getting dynamic class loaders")
        try:
            self._query_class_loader = ClassLoader(
                items=reader.items(section="query-classes")
            )
            self._format_class_loader = ClassLoader(
                items=reader.items(section="format-classes")
            )
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log_init_done()

    @property
    def query_options(self):
        """Get query_options."""
        return self._options["query_"]

    @property
    def format_options(self):
        """Get format opts."""
        return self._options["format_"]

    @property
    def query_class_loader(self):
        """Get query class loader object."""
        return self._query_class_loader

    @property
    def format_class_loader(self):
        """Get format class loader object."""
        return self._format_class_loader

    @property
    def query_class(self):
        """Get the configured query class."""
        try:
            return self.query_class_loader.get_class(
                name=self.query_options.class_name
            )
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e

    @property
    def format_class(self):
        """Get the configured format class."""
        try:
            return self.format_class_loader.get_class(
                name=self.format_options.class_name
            )
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e

    @staticmethod
    def _find_config_file():
        """Search for a config file at default locations."""
        dirs = [
            os.path.join(os.path.join(sys.prefix, "etc"), "rptk"),
            os.path.dirname(os.path.realpath(__file__))
        ]
        for dir in dirs:
            path = os.path.join(dir, "rptk.conf")
            if os.path.isfile(path):
                return path
        return None

    def _read_config(self):
        """Read the config file."""
        self.log_method_enter(method=self.current_method)
        reader = configparser.SafeConfigParser()
        self.log.debug(
            msg="trying to read configuration from file {}"
                .format(self.config_file)
        )
        try:
            reader.read(self.config_file)
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log_method_exit(method=self.current_method)
        return reader

    @property
    def config_file(self):
        """Get config file path."""
        return self._config_file

    def update(self, **kwargs):
        """Update self.opts from keyword args."""
        self.log_method_enter(method=self.current_method)
        for key, value in kwargs.items():
            for prefix, namespace in self._options.items():
                if key.startswith(prefix):
                    self.log.debug(msg="setting {} = {}".format(key, value))
                    setattr(namespace, key.lstrip(prefix), value)
        self.log_method_exit(method=self.current_method)
        return self

    def query(self, obj=None, name=None, test=False):
        """Perform a query and return the formatted output."""
        self.log_method_enter(method=self.current_method)
        if not name:
            self.log.debug(msg="name not provided using object ({})"
                               .format(obj))
            if obj:
                name = obj
            else:
                name = self.query_options.object
        self.log.debug(msg="trying to begin query")
        try:
            with self.query_class(**vars(self.query_options)) as q:
                result = q.query(obj=obj)
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log.debug(msg="trying to format result for output")
        try:
            with self.format_class(**vars(self.format_options)) as f:
                output = f.format(result=result, name=name)
                if test:
                    return f.validate(output=output)
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log_method_exit(method=self.current_method)
        return output
