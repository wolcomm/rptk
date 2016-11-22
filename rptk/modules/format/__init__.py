import logging
from rptk.configuration import Config


class BaseFormat(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config
        self._log = logging.getLogger(__name__)
        self._log.addHandler(config.logging_handler)

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

    def format(self, result=None, name=None):
        if not isinstance(result, dict):
            raise TypeError("%s not of type %s" % (result, dict))
        if not isinstance(name, basestring):
            raise TypeError("%s not of type %s" % (name, basestring))
        return None
