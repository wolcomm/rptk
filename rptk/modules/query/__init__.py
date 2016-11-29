from rptk import _BaseObject
from rptk.configuration import Config


class BaseQuery(_BaseObject):
    posix_only = False

    def __init__(self, config=None, **opts):
        super(BaseQuery, self).__init__()
        self.log_init()
        self._opts = opts
        if config:
            if not isinstance(config, Config):
                self.raise_type_error(arg=config, cls=Config)
            self.log.debug("initialising with config object %s" % config)
            self._config = config
        self.log_init_done()

    @property
    def config(self):
        try:
            return self._config
        except AttributeError as e:
            self.log.warning(msg=e.message)
            return None

    def query(self, obj=None):
        self.log_method_enter(method=self.current_method)
        if not obj:
            self.log.debug(msg="using object from configuration")
            if self.config:
                obj = self.config.args.object
            else:
                obj = self.opts["object"]
        if not isinstance(obj, basestring):
            self.raise_type_error(arg=obj, cls=basestring)
        return unicode(obj)

    @property
    def host(self):
        return self.opts["host"]

    @property
    def port(self):
        return int(self.opts["port"])

    @property
    def target(self):
        if self.config:
            return "%s:%s" % (self.config.args.host, self.config.args.port)
        else:
            return "%s:%s" % (self.host, self.port)
