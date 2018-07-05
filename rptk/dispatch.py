import os
import sys
import ConfigParser
from rptk.base import BaseObject
from rptk.load import ClassLoader


class Dispatcher(BaseObject):
    def __init__(self, **kwargs):
        super(Dispatcher, self).__init__()
        self.log_init()
        self._opts = dict()
        default_config_file = self._find_config_file()
        self._config_file = kwargs.pop("config_file", default_config_file)
        self.log.debug(msg="reading config file")
        reader = self._read_config()
        self.log.debug(msg="getting default options")
        opts = dict(reader.items("defaults"))
        self.log.debug(msg="updating options with user supplied values")
        opts.update(kwargs)
        self.update(**opts)
        self.log.debug(msg="getting dynamic class loaders")
        try:
            self._query_class_loader = ClassLoader(
                items=reader.items(section="query-classes")
            )
            self._format_class_loader = ClassLoader(
                items=reader.items(section="format-classes")
            )
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log_init_done()

    def _read_config(self):
        self.log_method_enter(method=self.current_method)
        reader = ConfigParser.SafeConfigParser()
        self.log.debug(
            msg="trying to read configuration from file %s" % self.config_file
        )
        try:
            reader.read(self.config_file)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log_method_exit(method=self.current_method)
        return reader

    def update(self, **opts):
        self.log_method_enter(method=self.current_method)
        self._opts.update(opts)
        for key in self.opts:
            try:
                if key[0] == '_':
                    raise ValueError("illegal option key: %s" % key)
                val = self.opts[key]
                if val:
                    self.log.debug(msg="updating option: %s = %s" % (key, val))
                    setattr(self, key, val)
            except Exception as e:
                self.log.error(msg=e.message)
                raise e
        self.log_method_exit(method=self.current_method)
        return self

    @property
    def config_file(self):
        return self._config_file

    @property
    def query_class_loader(self):
        return self._query_class_loader

    @property
    def format_class_loader(self):
        return self._format_class_loader

    @property
    def query_class(self):
        try:
            return self.query_class_loader.get_class(
                name=self.query
            )
        except Exception as e:
            self.log.error(msg=e.message)
            raise e

    @property
    def format_class(self):
        try:
            return self.format_class_loader.get_class(
                name=self.format
            )
        except Exception as e:
            self.log.error(msg=e.message)
            raise e

    @staticmethod
    def _find_config_file():
        dirs = [
            os.path.join(os.path.join(sys.prefix, "etc"), "rptk"),
            os.path.dirname(os.path.realpath(__file__))
        ]
        for dir in dirs:
            path = os.path.join(dir, "rptk.conf")
            if os.path.isfile(path):
                return path
        return None

    def dispatch(self, obj=None, name=None, test=False):
        self.log_method_enter(method=self.current_method)
        if not name:
            self.log.debug(msg="name not provided using object (%s)" % obj)
            if obj:
                name = obj
            else:
                name = self.opts["object"]
        self.log.debug(msg="trying to begin query")
        try:
            with self.query_class(**self.opts) as q:
                result = q.query(obj=obj)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log.debug(msg="trying to format result for output")
        try:
            with self.format_class(**self.opts) as f:
                output = f.format(result=result, name=name)
                if test:
                    return f.validate(output=output)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log_method_exit(method=self.current_method)
        return output
