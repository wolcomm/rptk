import json
import subprocess
from whichcraft import which
from rptk.configuration import ConfigSection, NewConfig


class BaseQuerier(object):
    def __init__(self, config=None):
        if not isinstance(config, NewConfig):
            raise TypeError("%s not of type %s" % (config, NewConfig))
        self._config = config

    @property
    def target(self):
        return "%s:%s" % (self._config.args.host, self._config.args.port)

    def query(self, obj=None):
        if not isinstance(obj, str):
            raise TypeError("%s not of type %s" % (obj, str))
        result = {
            'object': obj
        }
        return result


class Bgpq3Querier(BaseQuerier):
    def query(self, obj=None):
        super(Bgpq3Querier, self).query(obj=obj)
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
