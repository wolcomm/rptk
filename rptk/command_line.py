import sys
from logging import StreamHandler
from rptk import configuration, dispatch


def main():
    argv = sys.argv[1:]
    logging_handler = StreamHandler()
    config = configuration.Config(argv=argv, logging_handler=logging_handler)
    dispatcher = dispatch.Dispatcher(config=config)
    result = dispatcher.dispatch()
    sys.stdout.write("%s\n" % result)
    return


if __name__ == "__main__":
    main()
