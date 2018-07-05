from rptk import dispatch


class Rptk(object):
    def __init__(self, **opts):
        self._dispatcher = dispatch.Dispatcher(**opts)

    def query(self, obj=None, name=None, test=False):
        return self._dispatcher.dispatch(obj=obj, name=name, test=test)

    def available_formats(self):
        return self._dispatcher.format_class_loader.class_info

    def available_policies(self):
        return ('strict', 'loose',)

    def update_opts(self, **opts):
        try:
            self._dispatcher.update(**opts)
        except Exception as e:
            raise e
        return self

    @property
    def query_class_loader(self):
        return self._dispatcher.query_class_loader

    @property
    def format_class_loader(self):
        return self._dispatcher.format_class_loader

    @property
    def opts(self):
        return self._dispatcher.opts

    def __getattribute__(self, name):
        try:
            return super(Rptk, self).__getattribute__(name)
        except AttributeError as e:
            try:
                return self.opts[name]
            except KeyError:
                pass
            raise e

    def __setattr__(self, name, value):
        try:
            self._dispatcher.update(**{name: value})
        except Exception:
            super(Rptk, self).__setattr__(name, value)
