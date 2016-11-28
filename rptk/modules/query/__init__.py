from rptk import _BaseObject
from rptk.configuration import Config


class BaseQuery(_BaseObject):
    posix_only = False

    def __init__(self, config=None):
        super(BaseQuery, self).__init__()
        self.log_init()
        if not isinstance(config, Config):
            self.raise_type_error(arg=config, cls=Config)
        self.log.debug("initialising with config object %s" % config)
        self._config = config
        self.log_ready()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def config(self):
        return self._config

    def query(self, obj=None):
        self.log_enter(method=self.current_method)
        if not obj:
            self.log.debug(msg="using object from configuration")
            obj = self.config.args.object
        if not isinstance(obj, basestring):
            self.raise_type_error(arg=obj, cls=basestring)
        return unicode(obj)
