from rptk import dispatch


class Rptk(object):
    def __init__(self, **opts):
        self._dispatcher = dispatch.Dispatcher(**opts)

    def query(self, obj=None, name=None, test=False):
        return self._dispatcher.dispatch(obj=obj, name=name, test=test)

    def available_formats(self):
        return self._dispatcher.format_class_loader.class_names

    @property
    def opts(self):
        return self._dispatcher.opts

    def __getattribute__(self, name):
        if name in self.opts:
            return self.opts[name]
        else:
            return super(Rptk, self).__getattribute__(name)

    def __setattr__(self, name, value):
        try:
            self._dispatcher.update(**{name: value})
        except Exception as e:
            super(Rptk, self).__setattr__(name, value)
