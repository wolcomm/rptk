from daemonize import Daemonize
from time import sleep


def init():
    pid_file = __name__ + ".pid"
    daemon = Daemonize(app=__name__, action=loop, pid=pid_file)
    daemon.start()


def loop():
    while True:
        print "running..."
        sleep(10)
    return

if __name__ == "__main__":
    init()
