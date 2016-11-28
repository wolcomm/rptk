import json
import subprocess
from rptk.modules.query import BaseQuery
from whichcraft import which


class Bgpq3Query(BaseQuery):
    posix_only = True

    def query(self, obj=None):
        obj = super(Bgpq3Query, self).query(obj=obj)
        result = dict()
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
            result.update(json.loads(subprocess.check_output(cmds[key])))
        self.log_method_exit(method=self.current_method)
        return result

    @property
    def path(self):
        self.log.debug(msg="determining bgpq3 executable path")
        try:
            return self.config.args.bgpq3_path
        except AttributeError:
            self.log.debug(msg="no configured path, using system default")
            return which("bgpq3")

    @property
    def target(self):
        return "%s:%s" % (self.config.args.host, self.config.args.port)

