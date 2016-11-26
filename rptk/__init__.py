import logging
import inspect

logging.getLogger(__name__).addHandler(
    logging.NullHandler()
)


class _BaseObject(object):
    def __init__(self):
        self._log = logging.getLogger(self.__module__)

    @property
    def log(self):
        return self._log

    @property
    def cls_name(self):
        return self.__class__.__name__

    @property
    def current_method(self):
        return inspect.currentframe().f_back.f_code.co_name

    def log_init(self):
        self.log.debug(msg="initialising %s instance" % self.cls_name)

    def log_ready(self):
        self.log.debug(msg="%s instance ready" % self.cls_name)

    def log_enter(self, method=None):
        self.log.debug(msg="entering method %s.%s" % (self.cls_name, method))

    def log_exit(self, method=None):
        self.log.debug(msg="leaving method %s.%s" % (self.cls_name, method))
