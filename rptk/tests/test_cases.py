import os
import importlib
import ConfigParser
from unittest import TestCase
from rptk import configuration, dispatch, load


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

    def test_02_dispatch_to_classes(self):
        cfg = ConfigParser.SafeConfigParser()
        cfg.read(self.config_path)
        query_class_loader = load.ClassLoader(items=cfg.items("query-classes"))
        format_class_loader = load.ClassLoader(items=cfg.items("format-classes"))
        for q in query_class_loader.class_names:
            query_class = query_class_loader.get_class(name=q)
            if query_class.posix_only and not self.posix:
                continue
            for f in format_class_loader.class_names:
                opts = {'query': q, 'format': f}
                config = configuration.Config(argv=self.argv, opts=opts)
                dispatcher = dispatch.Dispatcher(config=config)
                result = dispatcher.dispatch(test=True)
                self.assertTrue(result)
