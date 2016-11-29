from rptk import _BaseObject
from rptk.configuration import Config


class Dispatcher(_BaseObject):
    def __init__(self, config=None):
        super(Dispatcher, self).__init__()
        self.log_init()
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self.log.debug("initialising with config object %s" % config)
        self._config = config
        self.log_init_done()

    @property
    def config(self):
        return self._config

    def dispatch(self, obj=None, name=None, test=False):
        self.log_method_enter(method=self.current_method)
        if obj and not name:
            self.log.debug(msg="name not provided using object (%s)" % obj)
            name = obj
        self.log.debug(msg="trying to begin query")
        try:
            with self.config.args.query_class(config=self.config) as q:
                result = q.query(obj=obj)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log.debug(msg="trying to format result for output")
        try:
            with self.config.args.format_class(config=self.config) as f:
                output = f.format(result=result, name=name)
                if test:
                    return f.validate(output=output)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log_method_exit(method=self.current_method)
        return output
