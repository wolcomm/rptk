import json
import subprocess
from rptk.modules.query import BaseQuery
from whichcraft import which


class Bgpq3Query(BaseQuery):
    def query(self, obj=None):
        super(Bgpq3Query, self).query(obj=obj)
        result = dict()
        if not self.path:
            raise RuntimeError("couldn't determine bgpq3 executable path")
        cmds = {
            'ipv4': [self.path, "-h", self.target, "-l", "ipv4", "-4Aj", obj],
            'ipv6': [self.path, "-h", self.target, "-l", "ipv6", "-6Aj", obj]
        }
        for key in cmds:
            result.update(json.loads(subprocess.check_output(cmds[key])))
        return result

    @property
    def path(self):
        try:
            return self._config.args.bgpq3_path
        except AttributeError:
            return which("bgpq3")
