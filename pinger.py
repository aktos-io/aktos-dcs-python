__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg.text, msg.timestamp
        sleep(2)
        self.send(PongMessage(text="Hello ponger, this is pinger 1!"))


if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger..."))
    joinall([pinger])
