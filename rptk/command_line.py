import sys
from rptk import parse, configuration, dispatch


def main():
    args = parse.Parser().args
    config = configuration.Config(args=args)
    dispatcher = dispatch.Dispatcher(config=config)
    result = dispatcher.dispatch()
    sys.stdout.write(result)
    return


if __name__ == "__main__":
    main()
