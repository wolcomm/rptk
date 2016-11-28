import jinja2
from rptk import _BaseObject
from rptk.configuration import Config


class BaseFormat(_BaseObject):
    def __init__(self, config=None):
        super(BaseFormat, self).__init__()
        self.log_init()
        if not isinstance(config, Config):
            self.raise_type_error(arg=config, cls=Config)
        self.log.debug("initialising with config object %s" % config)
        self._config = config
        self.log_init_done()

    @property
    def config(self):
        return self._config

    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        if not isinstance(result, dict):
            self.raise_type_error(arg=result, cls=dict)
        if not name:
            self.log.debug(msg="using name from configuration")
            name = self.config.args.name
        if not isinstance(name, basestring):
            self.raise_type_error(arg=name, cls=basestring)
        output = unicode(name)
        self.log_method_exit(method=self.current_method)
        return output

    def validate(self, output=None):
        self.log_method_enter(method=self.current_method)
        if not isinstance(output, basestring):
            self.raise_type_error(arg=output, cls=basestring)
        self.log.debug(msg="validation successful")
        self.log_method_exit(method=self.current_method)
        return True


class JinjaFormat(BaseFormat):
    template_name = None

    def __init__(self, config=None):
        super(JinjaFormat, self).__init__(config=config)
        self.log.debug("configuring jinja2 environment")
        try:
            self.env = jinja2.Environment(
                loader=jinja2.PackageLoader('rptk')
            )
            self.env.trim_blocks = True
            self.env.lstrip_blocks = True
        except Exception as e:
            self.raise_runtime_error(e.message)
        self._template = None
        self.log_init_done()

    def __enter__(self):
        self.log_ready_start()
        self._load_template()
        self.log_ready_done()
        return self

    @property
    def template(self):
        return self._template

    def _load_template(self):
        try:
            self._template = self.env.get_template(self.template_name)
        except jinja2.TemplateError as e:
            self.log.error(msg=e.message)
            raise
        self.log.debug("template loaded successfully")

    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        name = super(JinjaFormat, self).format(result=result, name=name)
        if isinstance(self.template, jinja2.Template):
            try:
                output = self.template.render(result=result, name=name)
                self.log_method_exit(method=self.current_method)
                return output
            except Exception as e:
                self.log.error(msg=e.message)
                raise
        else:
            self.raise_type_error(arg=self.template, cls=jinja2.Template)
