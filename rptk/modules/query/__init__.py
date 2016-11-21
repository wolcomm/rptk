from rptk.configuration import Config


class BaseQuery(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
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
