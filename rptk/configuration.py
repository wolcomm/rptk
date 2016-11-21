import os
import importlib
import ConfigParser
import argparse


class Config(object):
    def __init__(self, argv=None, opts=None):
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
        query_classes = self._register_classes(config.items("query-classes"))
        format_classes = self._register_classes(config.items("format-classes"))
        parser.set_defaults(**defaults)
        parser.add_argument(
            '--query', '-Q', action='store', type=str,
            help="query class", choices=query_classes.keys()
        )
        parser.add_argument(
            '--format', '-F', action='store', type=str,
            help="format class", choices=format_classes.keys()
        )
        parser.add_argument('--host', action='store', type=str, help="irrd host to connect to")
        parser.add_argument('--port', action='store', type=int, help="irrd service tcp port")
        parser.add_argument('--name', action='store', type=str, help="prefix-list name (default: object)")
        parser.add_argument('--help', action='help', help="print usage information and exit")
        parser.add_argument('object', nargs='?', action='store', type=str, help="rpsl object name")
        args = parser.parse_args(args=remaining_args)
        if not args.object:
            raise RuntimeError("No default value provided for object")
        if not args.name:
            args.name = args.object
        args.query_class = query_classes[args.query]
        args.format_class = format_classes[args.format]
        self._args = args

    @property
    def args(self):
        return self._args

    def _register_classes(self, entries=None):
        classes = dict()
        for entry in entries:
            name = entry[0]
            mod_path, cls_path = entry[1].rsplit(".", 1)
            cls = getattr(importlib.import_module(mod_path), cls_path)
            classes.update({name: cls})
        return classes
