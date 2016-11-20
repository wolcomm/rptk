import os
import ConfigParser
import argparse


class Config(object):
    def __init__(self, argv=None, opts=None):
        if not argv:
            argv = list()
        parser = argparse.ArgumentParser()
        defaults_config = ConfigParser.SafeConfigParser()
        default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rptk.conf')
        parser.add_argument(
            '--config_path', '-f', action='store', type=str,
            help="path to configuration file", default=default_config_path
        )
        partial_args, remaining_args = parser.parse_known_args(args=argv)
        defaults_config.read(partial_args.config_path)
        try:
            defaults = dict(defaults_config.items("defaults"))
        except ConfigParser.Error:
            raise
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
        parser.add_argument('object', nargs='?', action='store', type=str, help="print prefix list for OBJECT and exit")
        self._args = parser.parse_args(args=remaining_args)

    @property
    def args(self):
        return self._args
