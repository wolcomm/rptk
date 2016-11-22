import logging
import jinja2
from rptk.configuration import Config


class BaseFormat(object):
    def __init__(self, config=None):
        if not isinstance(config, Config):
            raise TypeError("%s not of type %s" % (config, Config))
        self._config = config
        self._log = logging.getLogger(__name__)
        self._log.addHandler(config.logging_handler)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def config(self):
        return self._config

    @property
    def log(self):
        return self._log

    def format(self, result=None, name=None):
        if not isinstance(result, dict):
            raise TypeError("%s not of type %s" % (result, dict))
        if not isinstance(name, basestring):
            raise TypeError("%s not of type %s" % (name, basestring))
        return None


class JinjaFormat(BaseFormat):
    template_name = None

    def __init__(self, config=None):
        super(JinjaFormat, self).__init__(config=config)
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader('rptk')
        )
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self._template = None

    @property
    def template(self):
        return self._template

    def load_template(self):
        self._template = self.env.get_template(self.template_name)

    def format(self, result=None, name=None):
        super(JinjaFormat, self).format(result=result, name=name)
        self.load_template()
        if isinstance(self.template, jinja2.Template):
            output = self.template.render(result=result, name=name)
        else:
            raise TypeError("%s not of type %s" % (self.template, jinja2.Template))
        return output
