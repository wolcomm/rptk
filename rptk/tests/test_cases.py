import os
import importlib
import ConfigParser
from unittest import TestCase
from rptk import configuration, dispatch


class TestRptk(TestCase):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests.conf')
    argv = ['--config_path', config_path]
    if os.name == 'posix':
        posix = True
    else:
        posix = False

    def test_01_configure(self):
        config = configuration.Config(argv=self.argv)
        self.assertIsInstance(config, configuration.Config, msg="config object invalid")

    def test_02_query_classes(self):
        cfg = ConfigParser.SafeConfigParser()
        cfg.read(self.config_path)
        classes = {'query': {}, 'format': {}}
        for entry in cfg.items("query-classes"):
            name = entry[0]
            mod_path, cls_path = entry[1].rsplit(".", 1)
            cls = getattr(importlib.import_module(mod_path), cls_path)
            classes['query'].update({name: cls})
        for name in classes['query']:
            if classes['query'][name].posix_only and not self.posix:
                continue
            opts = {'query': name}
            config = configuration.Config(argv=self.argv, opts=opts)
            dispatcher = dispatch.Dispatcher(config=config)
            result = dispatcher.dispatch()
            self.assertIsInstance(result, dict)
