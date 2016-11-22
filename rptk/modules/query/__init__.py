import logging
from rptk.configuration import Config


class BaseQuery(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config
        self._log = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def config(self):
        return self._config

    @property
    def log(self):
        return self._log

    @property
    def target(self):
        return "%s:%s" % (self.config.args.host, self.config.args.port)

    def query(self, obj=None):
        if not isinstance(obj, str):
            raise TypeError("%s not of type %s" % (obj, str))
        result = {
            'object': obj
        }
        return result
