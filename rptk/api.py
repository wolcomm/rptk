from rptk import configuration, dispatch


class Rptk(object):
    def __init__(self, **kwargs):
        self.opts = kwargs
        self.config = configuration.Config(opts=self.opts)
        self.dispatcher = dispatch.Dispatcher(config=self.config)

    def query(self, obj=None, name=None, test=False):
        return self.dispatcher.dispatch(obj=obj, name=name, test=test)
