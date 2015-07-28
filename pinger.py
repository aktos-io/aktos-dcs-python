__author__ = 'ceremcem'

from aktos_dcs import *

class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(1)
        self.send(PongMessage(text="Hello ponger, this is pinger cca!"))

if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger cca..."))

    pinger.join()