import json
from rptk.configuration import Config


class BaseFormatter(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config

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


class IosFormatter(BaseFormatter):
    def format(self, result=None, name=None):
        super(IosFormatter, self).format(result=result, name=name)
        output = str()
        for af in result:
            i = 0
            for entry in result[af]:
                i += 10
                output += self.line(name=name, af=af, entry=entry, i=i)
        return output

    def line(self, name='Prefix-List', af=None, entry=None, i=None):
        if not isinstance(entry, dict):
            raise ValueError("%s not of type %s" % (entry, dict))
        if not isinstance(i, int):
            raise ValueError("%s not of type %s" % (i, int))
        return "%s %s seq %s permit %s\n" % (self.af(af=af), name, i, entry['prefix'])

    def af(self, af=None):
        if af == 'ipv4':
            return 'ip prefix-list'
        elif af == 'ipv6':
            return 'ipv6 prefix-list'
        else:
            raise ValueError("%s is not a valid address-family name" % af)
