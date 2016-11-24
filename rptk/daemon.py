from time import sleep
from rptk.api import Rptk
from logging import FileHandler
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
    log_file = __name__ + ".log"
    logging_handler = FileHandler(log_file)
    rptk = Rptk(logging_handler=logging_handler, format="ios")
    while True:
        print rptk.query(obj="AS37271")
        sleep(3)
    return

if __name__ == "__main__":
    init()
