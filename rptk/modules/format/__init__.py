import jinja2
from datetime import datetime
from rptk.base import BaseObject
from rptk.modules import PrefixSet


class BaseFormat(BaseObject):
    description = None

    def __init__(self, **opts):
        super(BaseFormat, self).__init__()
        self.log_init()
        self._opts = opts
        self.log_init_done()

    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        # if not isinstance(result, PrefixSet):
        if not isinstance(result, dict):
            self.raise_type_error(arg=result, cls=PrefixSet)
        if not name:
            self.log.debug(msg="using name from configuration")
            name = self.name
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

    @property
    def name(self):
        return self.opts["name"]


class JinjaFormat(BaseFormat):
    template_name = None

    def __init__(self, **opts):
        super(JinjaFormat, self).__init__(**opts)
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
                output = self.template.render(result=result, name=name, now=datetime.now())
                self.log_method_exit(method=self.current_method)
                return output
            except Exception as e:
                self.log.error(msg=e.message)
                raise
        else:
            self.raise_type_error(arg=self.template, cls=jinja2.Template)
