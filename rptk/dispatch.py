from rptk.configuration import Config


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._querier = config.args.query_class(config=config)
        self._formatter = config.args.format_class(config=config)
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
