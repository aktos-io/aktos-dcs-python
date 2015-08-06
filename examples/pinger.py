import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(2)
        self.send(PongMessage(text="Hello ponger, this is pinger 1!"))

if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger 1..."))

    wait_all()
