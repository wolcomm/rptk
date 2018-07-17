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
"""rptk class loader test cases."""

from __future__ import print_function
from __future__ import unicode_literals

from helpers import default_format_classes, default_query_classes

import pytest

from rptk.base import BaseObject

class_sets = (
    default_query_classes().items(),
    default_format_classes().items(),
)


class TestClassLoader(object):
    """Test cases for rptk class loader classes."""

    @pytest.mark.parametrize("class_set", class_sets)
    def test_class_loader(self, class_set):
        """Test rptk class loader."""
        from rptk.load import ClassLoader
        loader = ClassLoader(items=class_set)
        assert isinstance(loader.class_names, list)
        for name, path in class_set:
            assert name in loader.class_names
            assert name in loader.class_info
            assert loader.class_info[name]
            assert issubclass(loader.get_class(name=name), BaseObject)
        assert isinstance(loader.classes, list)
        for cls in loader.classes:
            assert isinstance(cls, type)
