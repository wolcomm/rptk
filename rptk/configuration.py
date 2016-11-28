import os
import ConfigParser
import argparse
import logging
from rptk import _BaseObject
from rptk.load import ClassLoader


class Config(_BaseObject):
    def __init__(self, argv=None, opts=None, parser=None):
        super(Config, self).__init__()
        self.log_init()
        if not argv:
            self.log.debug(msg="no command line args received")
            argv = list()
        if not parser:
            parser = argparse.ArgumentParser(add_help=False)
        config = ConfigParser.SafeConfigParser()
        default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rptk.conf')
        parser.add_argument(
            '--config_path', '-f', action='store', type=str,
            help="path to configuration file", default=default_config_path
        )
        partial_args, remaining_args = parser.parse_known_args(args=argv)
        self.log.debug(msg="using config file %s" % partial_args.config_path)
        config.read(partial_args.config_path)
        try:
            defaults = dict(config.items("defaults"))
        except ConfigParser.Error as e:
            self.log.error(msg=e.message)
            raise e
        if opts:
            if not isinstance(opts, dict):
                self.raise_type_error(arg=opts, cls=dict)
            self.log.debug(msg="reading opts dictionary")
            defaults.update(opts)
        self.log.debug(msg="loading query classes")
        query_class_loader = self._get_loader(items=config.items("query-classes"))
        self.log.debug(msg="loading format classes")
        format_class_loader = self._get_loader(items=config.items("format-classes"))
        parser.set_defaults(**defaults)
        parser.add_argument(
            '--query', '-Q', action='store', type=str,
            help="query class", choices=query_class_loader.class_names
        )
        parser.add_argument(
            '--format', '-F', action='store', type=str,
            help="format class", choices=format_class_loader.class_names
        )
        parser.add_argument('--host', action='store', type=str, help="irrd host to connect to")
        parser.add_argument('--port', action='store', type=int, help="irrd service tcp port")
        parser.add_argument('--name', action='store', type=str, help="prefix-list name (default: object)")
        parser.add_argument('--help', action='help', help="print usage information and exit")
        parser.add_argument('object', nargs='?', action='store', type=str, help="rpsl object name")
        self.log.debug(msg="parsing %s command-line args" % len(remaining_args))
        args = parser.parse_args(args=remaining_args)
        if not args.object:
            self.log.debug(msg="no object provided")
            args.object = None
        if not args.name:
            self.log.debug(msg="no ouput name provided")
            args.name = args.object
        args.query_class = query_class_loader.get_class(args.query)
        args.format_class = format_class_loader.get_class(args.format)
        self._args = args
        self.log_init_done()

    @property
    def args(self):
        return self._args

    @property
    def log(self):
        return self._log

    def _get_loader(self, items=None):
        return ClassLoader(items=items)
