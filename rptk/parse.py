import argparse


class Parser(object):
    def __init__(self, args=None):
        program_name = "rptk"
        description = "tool for prefix filter list management operations"
        parser = argparse.ArgumentParser(prog=program_name, description=description)
        parser.add_argument('--querier_class_name', '-Q', action='store', type=str, help="querier class name")
        parser.add_argument('--formatter_class_name', '-F', action='store', type=str, help="formatter class name")
        parser.add_argument('--config_path', '-f', action='store', type=str, help="path to configuration file")
        parser.add_argument('--host', action='store', type=str, help="irrd host to connect to")
        parser.add_argument('--port', action='store', type=int, help="irrd service tcp port")
        parser.add_argument('--name', action='store', type=str, help="prefix-list name (default: object)")
        parser.add_argument('object', action='store', type=str, help="print prefix list for OBJECT and exit")
        self._parser = parser
        self._args = args

    @property
    def args(self):
        if self._args:
            return self._parser.parse_args(self._args)
        else:
            return self._parser.parse_args()
