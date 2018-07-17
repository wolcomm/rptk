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
"""rptk module.query.bgpq3.async module."""

from __future__ import print_function
from __future__ import unicode_literals

import asyncio
import collections
import json

from rptk.query.bgpq3._sync import _Bgpq3QuerySync


class _Bgpq3QueryAsync(_Bgpq3QuerySync):
    """Performs queries using bgpq3."""

    def _run_cmds(self, all_cmds):
        """Spawn bgpq3 subprocesses and return query results."""
        self.log_method_enter(method=self.current_method)
        result = collections.defaultdict(dict)
        semaphore = asyncio.Semaphore(value=self.max_concurrency)
        loop = asyncio.get_event_loop()
        tasks = list()
        for obj, cmds in all_cmds.items():
            for af, cmd in cmds.items():
                tasks.append(self._run_cmd_async(semaphore, obj, af, cmd))
        cmd_results = loop.run_until_complete(asyncio.gather(*tasks))
        for obj, af, output in cmd_results:
            result[obj].update(json.loads(output))
        self.log_method_exit(method=self.current_method)
        return dict(result)

    async def _run_cmd_async(self, semaphore, obj, af, cmd):  # noqa: E999
        """Spawn a subprocess and return the contents of stdout."""
        self.log_method_enter(method=self.current_method)
        try:
            async with semaphore:
                self.log.debug(msg="running {}".format(" ".join(cmd)))
                proc = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE
                )
                self.log.debug(msg="started {}".format(" ".join(cmd)))
                stdout, stderr = await proc.communicate()
                await proc.wait()
                self.log.debug(msg="done {}".format(" ".join(cmd)))
                output = stdout.decode()
        except Exception as e:
            self.log.error(msg="{}".format(e))
            raise e
        self.log_method_exit(method=self.current_method)
        return (obj, af, output)

    @property
    def max_concurrency(self):
        """Get the maximum allowed number of simulateously running queries."""
        try:
            return self.opts["max_concurrency"]
        except KeyError:
            return 4
