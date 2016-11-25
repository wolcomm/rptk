from rptk import configuration, dispatch


class Rptk(object):
    def __init__(self, **kwargs):
        logging_handler = kwargs.pop('logging_handler', None)
        self.opts = kwargs
        self.config = configuration.Config(opts=self.opts, logging_handler=logging_handler)
        self.dispatcher = dispatch.Dispatcher(config=self.config)

    def query(self, obj=None, name=None, test=False):
        return self.dispatcher.dispatch(obj=obj, name=name, test=test)
