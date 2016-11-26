import sys
import logging
from rptk import configuration, dispatch


def main():
    lh = logging.StreamHandler()
    lf = logging.Formatter(fmt="%(asctime)s %(name)s: %(levelname)s %(message)s")
    lh.setFormatter(lf)
    logging.getLogger().addHandler(lh)
    logging.getLogger().setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    log.debug(msg="started")
    argv = sys.argv[1:]
    log.debug(msg="have %s arguments" % len(argv))
    config = configuration.Config(argv=argv)
    log.debug(msg="configuration done")
    dispatcher = dispatch.Dispatcher(config=config)
    log.debug(msg="dispatcher ready")
    result = dispatcher.dispatch()
    log.debug(msg="got result length %s" % len(result))
    sys.stdout.write("%s\n" % result)
    return


if __name__ == "__main__":
    main()
