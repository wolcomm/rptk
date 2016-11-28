import sys
import logging
import argparse
from rptk import configuration, dispatch


def main():
    log = logging.getLogger(__name__)
    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '--debug', '-d', action='store_const', const=logging.DEBUG, dest='log_level',
            help="print debug logging output", default=logging.WARNING
        )
        args, argv = parser.parse_known_args()
        lh = logging.StreamHandler()
        lf = logging.Formatter(fmt="%(asctime)s %(name)s: %(levelname)s %(message)s")
        lh.setFormatter(lf)
        logging.getLogger().addHandler(lh)
        logging.getLogger().setLevel(args.log_level)
    except Exception as e:
        log.error(msg=e.message)
        return 1
    try:
        log.debug(msg="started")
        log.debug(msg="have %s arguments" % len(argv))
        config = configuration.Config(argv=argv, parser=parser)
        log.debug(msg="configuration done")
        dispatcher = dispatch.Dispatcher(config=config)
        log.debug(msg="dispatcher ready")
        result = dispatcher.dispatch()
        log.debug(msg="got result length %s" % len(result))
        sys.stdout.write("%s\n" % result)
        return 0
    except Exception as e:
        log.error(msg=e.message)
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
