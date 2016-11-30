import logging
from time import sleep
from rptk import RptkAPI
try:
    from daemonize import Daemonize
    can_daemonize = True
except ImportError:
    can_daemonize = False


def init():
    if can_daemonize:
        pid_file = __name__ + ".pid"
        daemon = Daemonize(app=__name__, action=main, pid=pid_file)
        daemon.start()
    else:
        main()


def main():
    # start logging
    log_file = __name__ + ".log"
    lh = logging.FileHandler(log_file)
    lf = logging.Formatter(fmt="%(asctime)s %(name)s: %(levelname)s %(message)s")
    lh.setFormatter(lf)
    logging.getLogger().addHandler(lh)
    # setup rptk api
    rptk = RptkAPI(format="ios")
    # begin loop
    while True:
        print rptk.query(obj="AS37271")
        sleep(3)
    return

if __name__ == "__main__":
    init()
