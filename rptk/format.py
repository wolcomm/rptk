import json
from rptk.configuration import ConfigSection


class BaseFormatter(object):
    def __init__(self, config=None):
        if not isinstance(config, ConfigSection):
            raise TypeError("%s not of type %s" % (config, ConfigSection))
        self.config = config

    def format(self, result=None, name=None):
        if not isinstance(result, dict):
            raise TypeError("%s not of type %s" % (result, dict))
        if not isinstance(name, str):
            raise TypeError("%s not of type %s" % (name, str))
        return None


class TestFormatter(BaseFormatter):
    def format(self, result=None, name=None):
        super(TestFormatter, self).format(result=result, name=name)
        output = {
            name: result
        }
        return output


class JsonFormatter(BaseFormatter):
    def format(self, result=None, name=None):
        super(JsonFormatter, self).format(result=result, name=name)
        output = json.dumps({name: result}, indent=4)
        return output
