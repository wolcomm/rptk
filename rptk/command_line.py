import sys
from rptk import configuration, dispatch


def main():
    argv = sys.argv[1:]
    config = configuration.Config(argv=argv)
    dispatcher = dispatch.Dispatcher(config=config)
    result = dispatcher.dispatch()
    sys.stdout.write(result)
    return


if __name__ == "__main__":
    main()
