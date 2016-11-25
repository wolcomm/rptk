import logging
from rptk.configuration import Config


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config
        self._log = logging.getLogger(__name__)
        self._log.addHandler(config.logging_handler)

    @property
    def config(self):
        return self._config

    @property
    def log(self):
        return self._log

    def dispatch(self, obj=None, name=None, test=False):
        if obj and not name:
            name = obj
        with self.config.args.query_class(config=self.config) as q:
            result = q.query(obj=obj)
        with self.config.args.format_class(config=self.config) as f:
            output = f.format(result=result, name=name)
            if test:
                return f.validate(output=output)
        return output
