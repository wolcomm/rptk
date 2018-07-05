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

from rptk import dispatch


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


def pre_parse():
    """Parse pre-configuration options."""
    parser = argparse.ArgumentParser(add_help=False,
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument('--debug', '-d', action='store_true',
                        help="print debug logging output")
    parser.add_argument('--config_file', '-f', type=str,
                        help="path to configuration file")
    args, args_remaining = parser.parse_known_args()
    return parser, args, args_remaining


def parse(parser, args_remaining, dispatcher):
    """Parse configuration options."""
    parser.add_argument('--query', '-Q', help="query class",
                        choices=dispatcher.query_class_loader.class_names)
    parser.add_argument('--format', '-F', help="format class",
                        choices=dispatcher.format_class_loader.class_names)
    parser.add_argument('--policy', '-P', type=str,
                        help="resolution policy",
                        choices=('strict', 'loose'))
    parser.add_argument('--host', '-h', type=str,
                        help="irrd host to connect to")
    parser.add_argument('--port', '-p', type=int,
                        help="irrd service tcp port")
    parser.add_argument('--name', '-n', type=str,
                        help="prefix-list name (default: object)")
    parser.add_argument('--help', action='help',
                        help="print usage information and exit")
    parser.add_argument('object', type=str, help="rpsl object name")
    args = parser.parse_args(args=args_remaining)
    return args


def main():
    """Execute a query."""
    # setup logger
    log = logging_init()
    rc = 2
    try:
        # get config_file and debug options
        parser, args, args_remaining = pre_parse()
        # set log level
        try:
            if args.debug:
                logging.getLogger().setLevel(logging.DEBUG)
                log.debug(msg="debug logging started")
        except AttributeError:
            pass
        # set up dispatcher with default options
        log.debug(msg="creating dispatcher object")
        dispatcher = dispatch.Dispatcher(**vars(args))
        log.debug(msg="dispatcher ready")
        # parse remaining args and update dispatcher options
        log.debug(msg="parsing command-line arguments")
        args = parse(parser=parser, args_remaining=args_remaining,
                     dispatcher=dispatcher)
        log.debug(msg="updating dispatcher options")
        dispatcher.update(**vars(args))
        # dispatch query and print formatted result
        log.debug(msg="dispatching query")
        result = dispatcher.dispatch()
        log.debug(msg="got result length {}".format(len(result)))
        sys.stdout.write("{}\n".format(result))
        rc = 0
    except Exception as e:
        log.error(msg="{}".format(e))
        rc = 1
    exit(rc)


if __name__ == "__main__":
    main()
