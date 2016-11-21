import os
from unittest import TestCase
from whichcraft import which
from rptk import configuration, dispatch


class TestRptk(TestCase):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests.conf')
    argv = ['--config_path', config_path]

    def test_01_dependency_bgpq3(self):
        path = which('bgpq3')
        self.assertIsInstance(path, str, msg="bgpq3 executable not found in PATH")

    def test_02_configure(self):
        config = configuration.Config(argv=self.argv)
        self.assertIsInstance(config, configuration.Config, msg="config object invalid")
        self.config = config

    def test_03_dummy_query(self):
        dispatcher = dispatch.Dispatcher(config=self.config)
        result = dispatcher.dispatch()
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["test"], dict)
        self.assertEqual(result["test"]["object"], self.config.args.object)
