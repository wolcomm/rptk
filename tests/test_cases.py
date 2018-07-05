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
"""rptk test cases."""

import os
import unittest

from rptk import RptkAPI


class TestRptk(unittest.TestCase):
    """Test cases for rptk."""

    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'tests.conf')
    if os.name == 'posix':
        posix = True
    else:
        posix = False

    def test_api(self):
        """Test rptk python API."""
        rptk = RptkAPI(config_file=self.config_file)
        for q in rptk.query_class_loader.class_names:
            query_class = rptk.query_class_loader.get_class(name=q)
            if query_class.posix_only and not self.posix:
                continue
            for f in rptk.format_class_loader.class_names:
                opts = {'query': q, 'format': f}
                rptk.update_opts(**opts)
                result = rptk.query(test=True)
                self.assertTrue(result)
                if result:
                    print "api query with query=%s format=%s passed" % (q, f)
