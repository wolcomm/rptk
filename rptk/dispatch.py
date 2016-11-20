from rptk.configuration import Config
from rptk import query, format


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        querier_class = getattr(query, config.args.querier)
        self._querier = querier_class(config=config)
        formatter_class = getattr(format, config.args.formatter)
        self._formatter = formatter_class(config=config)
        self._object = config.args.object
        self._name = config.args.name

    @property
    def querier(self):
        return self._querier

    @property
    def formatter(self):
        return self._formatter

    @property
    def object(self):
        return self._object

    @property
    def name(self):
        return self._name

    def dispatch(self):
        result = self.querier.query(obj=self.object)
        output = self.formatter.format(result=result, name=self.name)
        return output
