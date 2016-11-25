import os
import importlib
import ConfigParser
from unittest import TestCase
from whichcraft import which
from rptk import configuration, dispatch


class TestRptk(TestCase):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests.conf')
    argv = ['--config_path', config_path]
    if os.name == 'posix':
        posix = True
    else:
        posix = False

    def test_01_dependency_bgpq3(self):
        if self.posix:
            path = which('bgpq3')
            self.assertIsInstance(path, str, msg="bgpq3 executable not found in PATH")
        return

    def test_02_configure(self):
        config = configuration.Config(argv=self.argv)
        self.assertIsInstance(config, configuration.Config, msg="config object invalid")
        self.config = config

    def test_03_dummy_query(self):
        config = configuration.Config(argv=self.argv)
        dispatcher = dispatch.Dispatcher(config=config)
        result = dispatcher.dispatch()
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["test"], dict)
        self.assertEqual(result["test"]["object"], config.args.object)

    def test_04_query_classes(self):
        cfg = ConfigParser.SafeConfigParser()
        cfg.read(self.config_path)
        classes = dict()
        for entry in cfg.items("query-classes"):
            name = entry[0]
            mod_path, cls_path = entry[1].rsplit(".", 1)
            cls = getattr(importlib.import_module(mod_path), cls_path)
            classes.update({name: cls})
        for name in classes:
            if classes[name].posix_only and not self.posix:
                continue
            opts = {'query': name}
            config = configuration.Config(argv=self.argv, opts=opts)
            dispatcher = dispatch.Dispatcher(config=config)
            result = dispatcher.dispatch()
            self.assertIsInstance(result, dict)
