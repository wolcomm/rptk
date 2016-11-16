from rptk import parse, configuration, dispatch


def main():
    args = parse.Parser().args
    config = configuration.Config(args=args)
    dispatcher = dispatch.Dispatcher(config=config)
    return dispatcher.dispatch()


if __name__ == "__main__":
    result = main()
    print result
    exit()
