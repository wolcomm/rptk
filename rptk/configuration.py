import os
import importlib
import ConfigParser
import argparse
import logging
from rptk.load import ClassLoader


class Config(object):
    def __init__(self, argv=None, opts=None, logging_handler=None):
        if logging_handler:
            if isinstance(logging_handler, logging.Handler):
                self._logging_handler = logging_handler
            else:
                raise TypeError("%s not of type %s" % (logging_handler, logging.Handler))
        else:
            self._logging_handler = logging.NullHandler()
        self._log = logging.getLogger(__name__)
        self._log.addHandler(self.logging_handler)
        if not argv:
            argv = list()
        parser = argparse.ArgumentParser(add_help=False)
        config = ConfigParser.SafeConfigParser()
        default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rptk.conf')
        parser.add_argument(
            '--config_path', '-f', action='store', type=str,
            help="path to configuration file", default=default_config_path
        )
        partial_args, remaining_args = parser.parse_known_args(args=argv)
        config.read(partial_args.config_path)
        try:
            defaults = dict(config.items("defaults"))
        except ConfigParser.Error:
            raise
        if opts:
            if not isinstance(opts, dict):
                raise TypeError("%s not of type %s" % (opts, dict))
            defaults.update(opts)
        query_class_loader = ClassLoader(items=config.items("query-classes"))
        format_class_loader = ClassLoader(items=config.items("format-classes"))
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
        args = parser.parse_args(args=remaining_args)
        if not args.object:
            args.object = None
        if not args.name:
            args.name = args.object
        args.query_class = query_class_loader.get_class(args.query)
        args.format_class = format_class_loader.get_class(args.format)
        self._args = args

    @property
    def args(self):
        return self._args

    @property
    def logging_handler(self):
        return self._logging_handler

    @property
    def log(self):
        return self._log
