import json
import subprocess
from whichcraft import which
from rptk.modules import PrefixSet
from rptk.modules.query import BaseQuery


class Bgpq3Query(BaseQuery):
    posix_only = True

    def query(self, obj=None):
        obj = super(Bgpq3Query, self).query(obj=obj)
        tmp = dict()
        if not self.path:
            msg = "couldn't determine bgpq3 executable path"
            self.log.error(msg=msg)
            raise RuntimeError(msg)
        cmds = {
            'ipv4': [self.path, "-h", self.target, "-l", "ipv4", "-4Aj", obj],
            'ipv6': [self.path, "-h", self.target, "-l", "ipv6", "-6Aj", obj]
        }
        for key in cmds:
            self.log.debug(msg="running %s" % ' '.join(cmds[key]))
            tmp.update(json.loads(subprocess.check_output(cmds[key])))
        # result = PrefixSet(results=tmp)
        result = tmp
        self.log_method_exit(method=self.current_method)
        return result

    @property
    def path(self):
        self.log.debug(msg="determining bgpq3 executable path")
        try:
            return self.opts["bgpq3_path"]
        except KeyError:
            self.log.debug(msg="no configured path, using system default")
            return which("bgpq3")
