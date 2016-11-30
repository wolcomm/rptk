from rptk.base import BaseObject


class BaseQuery(BaseObject):
    posix_only = False

    def __init__(self, **opts):
        super(BaseQuery, self).__init__()
        self.log_init()
        self._opts = opts
        self.log_init_done()

    def query(self, obj=None):
        self.log_method_enter(method=self.current_method)
        if not obj:
            self.log.debug(msg="using object from configuration")
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
        return "%s:%s" % (self.host, self.port)
