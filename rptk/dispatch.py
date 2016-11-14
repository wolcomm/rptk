from rptk.configuration import Config
from rptk import query, format


class Dispatcher(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._querier = getattr(query, config.main.querier_class_name)(config=config.querier)
        self._formatter = getattr(format, config.main.formatter_class_name)(config=config.querier)
        self.object = config.object
        self.name = config.name

    def dispatch(self):
        result = self._querier.query(object=self.object)
        output = self._formatter.format(result=result, name=self.name)
        return output
