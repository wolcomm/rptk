from rptk import configuration, dispatch


class Rptk(object):
    def __init__(self, **kwargs):
        logging_handler = kwargs.pop('logging_handler', default=None)
        self.opts = kwargs
        self.config = configuration.Config(opts=self.opts, logging_handler=logging_handler)
        self.dispatcher = dispatch.Dispatcher(config=self.config)

    def query(self):
        return self.dispatcher.dispatch()
