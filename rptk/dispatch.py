from rptk.configuration import Config, NewConfig
from rptk import query, format


class NewDispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, NewConfig):
            raise TypeError("%s not of type %s" % (config, NewConfig))
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
        return self._name or self.object

    def dispatch(self):
        result = self.querier.query(obj=self.object)
        output = self.formatter.format(result=result, name=self.name)
        return output


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._querier = getattr(query, config.main.querier_class_name)(config=config.querier)
        self._formatter = getattr(format, config.main.formatter_class_name)(config=config.querier)
        self.object = config.object
        self.name = config.name

    def dispatch(self):
        result = self._querier.query(obj=self.object)
        output = self._formatter.format(result=result, name=self.name)
        return output
