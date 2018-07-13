# Copyright (c) 2018 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License version 2.0
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rptk command_line module."""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import sys

from rptk import RptkAPI


def logging_init():
    """Set up logger."""
    log = logging.getLogger(__name__)
    lh = logging.StreamHandler()
    lf = logging.Formatter(
        fmt="%(asctime)s %(name)s: %(levelname)s %(message)s"
    )
    lh.setFormatter(lf)
    logging.getLogger().addHandler(lh)
    return log


def pre_parse(argv):
    """Parse pre-configuration options."""
    parser = argparse.ArgumentParser(add_help=False,
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument('--debug', '-d', action='store_true', default=False,
                        help="print debug logging output")
    parser.add_argument('--version', '-v', action='store_true', default=False,
                        help="print version and exit")
    parser.add_argument('--config-file', '-f', type=str,
                        help="path to configuration file")
    args, args_remaining = parser.parse_known_args(argv)
    return parser, args, args_remaining


def parse(parser, args_remaining, api):
    """Parse configuration options."""
    parser.add_argument('--query', '-Q', dest='query_class_name',
                        help="query class",
                        choices=api.query_class_loader.class_names)
    parser.add_argument('--format', '-F', dest='format_class_name',
                        help="format class",
                        choices=api.format_class_loader.class_names)
    parser.add_argument('--policy', '-P', dest='query_policy', type=str,
                        help="resolution policy",
                        choices=api.available_policies)
    parser.add_argument('--host', '-h', dest='query_host', type=str,
                        help="irrd host to connect to")
    parser.add_argument('--port', '-p', dest='query_port', type=int,
                        help="irrd service tcp port")
    parser.add_argument('--name', '-n', dest='format_name', type=str,
                        help="prefix-list name (default: object)")
    parser.add_argument('query_objects', type=str, nargs="+",
                        help="rpsl object name")
    parser.add_argument('--help', action='help',
                        help="print usage information and exit")
    args = parser.parse_args(args=args_remaining)
    return args


def main(argv=sys.argv[1:]):
    """Execute a query."""
    # setup logger
    log = logging_init()
    rc = 2
    try:
        # get config_file and debug options
        log.debug(msg="got args: {}".format(argv))
        parser, args, args_remaining = pre_parse(argv)
        # set log level
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            log.debug(msg="debug logging started")
        else:
            logging.getLogger().setLevel(logging.WARNING)
        # print version if requested
        if args.version:
            sys.stdout.write("rptk version {}\n".format(RptkAPI.version))
            exit(0)
        # set up api with default options
        log.debug(msg="creating RptkAPI object")
        api = RptkAPI(**vars(args))
        log.debug(msg="RptkAPI instance ready")
        # parse remaining args and update api options
        log.debug(msg="parsing command-line arguments")
        args = parse(parser=parser, args_remaining=args_remaining, api=api)
        log.debug(msg="updating RptkAPI options")
        api.update(**vars(args))
        # execute query
        log.debug(msg="executing query")
        result = api.query(*args.query_objects)
        log.debug(msg="got result")
        # print formatted result
        log.debug(msg="formatting output")
        output = api.format(result=result)
        log.debug(msg="writing output to stdout")
        sys.stdout.write("{}\n".format(output))
        rc = 0
    except Exception as e:  # pragma: no cover
        log.error(msg="{}".format(e))
        rc = 1
    exit(rc)


if __name__ == "__main__":
    main()
