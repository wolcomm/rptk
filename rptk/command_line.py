import sys
from rptk import configuration, dispatch


def main():
    config = configuration.Config(argv=sys.argv)
    dispatcher = dispatch.Dispatcher(config=config)
    result = dispatcher.dispatch()
    sys.stdout.write(result)
    return


if __name__ == "__main__":
    main()
