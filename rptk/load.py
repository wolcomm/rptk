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
"""rptk load module."""

from __future__ import print_function
from __future__ import unicode_literals

import importlib

from rptk.base import BaseObject


class ClassLoader(BaseObject):
    """ClassLoader to dynamically load query and format classes."""

    def __init__(self, items=None):
        """Initialise a new ClassLoader object."""
        super(ClassLoader, self).__init__()
        self.log_init()
        if not isinstance(items, list):
            raise TypeError("{} not of type {}".format(items, list))
        self._classes = dict()
        count = 0
        self.log.debug(msg="trying to load classes")
        for name, path in items:
            mod_path, cls_path = path.rsplit(".", 1)
            self.log.debug(msg="loading class {}".format(cls_path))
            try:
                cls = getattr(importlib.import_module(mod_path), cls_path)
                self._classes.update({name: cls})
                count += 1
            except Exception as e:
                self.log.warning(msg="{}".format(e))
        self.log.debug(msg="loaded {} classes".format(count))
        self.log_init_done()

    def get_class(self, name=None):
        """Get the named class."""
        return self._classes[name]

    @property
    def class_names(self):
        """Get a list of avalable class names."""
        return [name for name in self._classes]

    @property
    def classes(self):
        """Get a list of available classes."""
        return [self.get_class(name) for name in self.class_names]

    @property
    def class_info(self):
        """Get a mapping of class names to descriptions."""
        info = dict()
        for name in self._classes:
            descr = None
            try:
                descr = self.get_class(name=name).description
            except AttributeError as e:
                self.log.debug(msg="{}".format(e))
            except Exception as e:
                self.log.error(msg="{}".format(e))
                raise e
            info.update({name: {
                'description': descr
            }})
        return info
