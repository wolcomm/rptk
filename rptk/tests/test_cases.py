import os
from unittest import TestCase
from whichcraft import which


class TestOutput(TestCase):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests-defaults.ini')

    def test_01_dependency(self):
        path = which('bgpq3')
        self.assertIsInstance(path, str, msg="bgpq3 executable not found in PATH")
