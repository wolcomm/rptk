from rptk.configuration import Config


class BaseFormat(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def format(self, result=None, name=None):
        if not isinstance(result, dict):
            raise TypeError("%s not of type %s" % (result, dict))
        if not isinstance(name, str):
            raise TypeError("%s not of type %s" % (name, str))
        return None
