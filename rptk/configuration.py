import os
import ConfigParser
import argparse
from argparse import Namespace


class NewConfig(object):
    def __init__(self, argv=None, opts=None):
        parser = argparse.ArgumentParser()
        defaults_config = ConfigParser.SafeConfigParser()
        defaults_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'new-defaults.ini')
        parser.add_argument(
            '--config_path', '-f', action='store', type=str,
            help="path to configuration file", default=defaults_path
        )
        if argv:
            if not isinstance(argv, list):
                raise TypeError("%s not of type %s" % (argv, list))
            partial_args, remaining_args = parser.parse_known_args(argv)
            defaults_path = partial_args.config_file
        else:
            remaining_args = None
        defaults_config.read(defaults_path)
        defaults = dict(defaults_config.items("defaults"))
        if opts:
            if not isinstance(opts, dict):
                raise TypeError("%s not of type %s" % (opts, dict))
            defaults.update(opts)
        parser.set_defaults(**defaults)
        parser.add_argument('--querier', '-Q', action='store', type=str, help="querier class name")
        parser.add_argument('--formatter', '-F', action='store', type=str, help="formatter class name")
        parser.add_argument('--host', action='store', type=str, help="irrd host to connect to")
        parser.add_argument('--port', action='store', type=int, help="irrd service tcp port")
        parser.add_argument('--name', action='store', type=str, help="prefix-list name (default: object)")
        parser.add_argument('object', action='store', type=str, help="print prefix list for OBJECT and exit")
        self._args = parser.parse_args(args=remaining_args)

    @property
    def args(self):
        return self._args


class Config(object):
    def __init__(self, args=None):
        if not isinstance(args, Namespace):
            raise TypeError("%s not of type %s" % (args, Namespace))
        self._args = args
        self._sections = set()
        defaults = ConfigParser.SafeConfigParser()
        defaults_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'defaults.ini')
        try:
            defaults.read(defaults_path)
            self._defaults = defaults
        except ConfigParser.Error:
            raise
        for section in self._defaults.sections():
            self._sections.add(section)
            cs = ConfigSection()
            setattr(self, section, cs)
            for option in self._defaults.options(section):
                value = self._defaults.get(section, option)
                cs.set(option, value)
        local = ConfigParser.SafeConfigParser()
        try:
            config_path = self._args.config_path
        except AttributeError:
            config_path = None
        if not config_path or not os.path.isfile(config_path):
            config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local-config.ini')
        try:
            local.read(config_path)
            self._local = local
        except ConfigParser.Error:
            self._local = None
        if self._local:
            for section in self._local.sections():
                cs = getattr(self, section)
                for option in self._local.options(section):
                    value = self._local.get(section, option)
                    cs.set(option, value)
        self.object = self._args.object
        self.name = self._args.name or self.object
        if self._args.querier_class_name:
            self.main.querier_class_name = self._args.querier_class_name
        if self._args.formatter_class_name:
            self.main.formatter_class_name = self._args.formatter_class_name


class ConfigSection(object):
    def __init__(self):
        self._options = set()

    def set(self, option=None, value=None):
        self._options.add(option)
        setattr(self, option, value)
