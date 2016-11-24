import logging
from rptk.configuration import Config


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config
        self._log = logging.getLogger(__name__)
        self._log.addHandler(config.logging_handler)
        self._query_class = config.args.query_class
        self._format_class = config.args.format_class
        self._object = config.args.object
        self._name = config.args.name

    @property
    def config(self):
        return self._config

    @property
    def log(self):
        return self._log

    def dispatch(self):
        with self.config.args.query_class(config=self.config) as q:
            result = q.query(obj=self.config.args.object)
        with self.config.args.format_class(config=self.config) as f:
            output = f.format(result=result, name=self.config.args.name)
        return output
