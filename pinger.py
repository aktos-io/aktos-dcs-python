__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg.msg_id, (time.time() - msg.timestamp), msg.debug
        sleep(1)
        self.send(PongMessage(text="Hello ponger, this is pinger 1!"))

if __name__ == "__main__":
    ProxyActor(brokers="192.168.2.119:5012:5013")
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger cca..."))

    pinger.join()