__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Ping got pong message: ", msg.text
        sleep(5)
        self.send(PongMessage(text="Hello ponger!"))


if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger..."))
    joinall([pinger])
