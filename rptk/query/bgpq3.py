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
"""rptk module.query.bgpq3 module."""

from __future__ import print_function
from __future__ import unicode_literals

import json
import subprocess

from rptk.query import BaseQuery

from whichcraft import which


class Bgpq3Query(BaseQuery):
    """Performs queries using bgpq3."""

    posix_only = True

    def query(self, *objects):
        """Execute a query."""
        objects = super(Bgpq3Query, self).query(*objects)
        if not self.path:
            msg = "couldn't determine bgpq3 executable path"
            self.log.error(msg=msg)
            raise RuntimeError(msg)
        try:
            policy = self.opts["policy"]
        except KeyError:
            policy = None
        result = dict()
        for obj in objects:
            tmp = dict()
            if policy == "loose":
                cmds = {
                    'ipv4': [
                        self.path,
                        "-h", self.target,
                        "-l", "ipv4", "-m", "24", "-r", "8", "-R", "24",
                        "-4Aj", obj
                    ],
                    'ipv6': [
                        self.path,
                        "-h", self.target,
                        "-l", "ipv6", "-m", "48", "-r", "16", "-R", "48",
                        "-6Aj", obj
                    ]
                }
            else:
                cmds = {
                    'ipv4': [
                        self.path,
                        "-h", self.target,
                        "-l", "ipv4", "-m", "24",
                        "-4Aj", obj
                    ],
                    'ipv6': [
                        self.path,
                        "-h", self.target,
                        "-l", "ipv6", "-m", "48",
                        "-6Aj", obj
                    ]
                }
            for af, cmd in cmds.items():
                self.log.debug(msg="running {}".format(" ".join(cmd)))
                try:
                    output = subprocess.check_output(cmd,
                                                     universal_newlines=True)
                except Exception as e:
                    self.log.error(msg="{}".format(e))
                tmp.update(json.loads(output))
            result.update({obj: tmp})
        self.log_method_exit(method=self.current_method)
        return result

    @property
    def path(self):
        """Find the path of the bgpq3 executable."""
        self.log.debug(msg="determining bgpq3 executable path")
        try:
            return self.opts["bgpq3_path"]
        except KeyError:
            self.log.debug(msg="no configured path, using system default")
            return which("bgpq3")
