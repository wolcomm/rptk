import os
import ConfigParser
from rptk import _BaseObject


class Dispatcher(_BaseObject):
    def __init__(self, **kwargs):
        super(Dispatcher, self).__init__()
        self.log_init()
        self.config_file = kwargs.pop(
            key="config_path",
            default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rptk.conf')
        )
        self.log.debug(msg="getting default options")
        opts = self.get_defaults()
        self.log.debug(msg="updating options with user supplied values")
        opts.update(other=kwargs)
        self.update(**opts)
        self.log_init_done()

    def get_defaults(self):
        self.log_method_enter(method=self.current_method)
        reader = ConfigParser.SafeConfigParser()
        self.log.debug(msg="reading configuration from file %s" % self.config_file)
        reader.read(self.config_file)
        defaults = dict(reader.items(section="defaults"))
        self.log.debug(msg="got %d key-value-pairs" % len(defaults))
        self.log_method_exit(method=self.current_method)
        return defaults

    def update(self, **kwargs):
        self.log_method_enter(method=self.current_method)
        for key in kwargs:
            self.log.debug(msg="updating option: %s = %s" % (key, kwargs[key]))
            setattr(self, name=key, value=kwargs[key])
        self.log_method_exit(method=self.current_method)
        return self

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
