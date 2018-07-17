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
        for batch in self._batches(all_cmds):
            self.log.debug(msg="processing batch {}"
                               .format([i[0] for i in batch]))
            loop = asyncio.get_event_loop()
            tasks = list()
            for obj, cmds in batch:
                for af, cmd in cmds.items():
                    tasks.append(self._run_cmd_async(obj, af, cmd))
            cmd_results = loop.run_until_complete(asyncio.gather(*tasks))
            loop.close()
            for obj, af, output in cmd_results:
                result[obj].update(json.loads(output))
        self.log_method_exit(method=self.current_method)
        return dict(result)

    def _batches(self, all_cmds, batch_size=2):
        """Create a generator of fixed size batches."""
        self.log_method_enter(method=self.current_method)
        items = list(all_cmds.items())
        for i in range(0, len(all_cmds), batch_size):
            yield items[i:i + batch_size]
        self.log_method_exit(method=self.current_method)

    async def _run_cmd_async(self, obj, af, cmd):
        """Spawn a subprocess and return the contents of stdout."""
        self.log_method_enter(method=self.current_method)
        self.log.debug(msg="running {}".format(" ".join(cmd)))
        try:
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
