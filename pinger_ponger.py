__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Pong got ping message:", msg.text
        sleep(5)
        self.send(PingMessage(text="Hello pinger!"))


class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Ping got pong message: ", msg.text
        sleep(5)
        self.send(PongMessage(text="Hello ponger!"))


if __name__ == "__main__":
    pinger = Pinger()
    ponger = Ponger()

    pinger.send(PongMessage(text="startup message from pinger..."))

    #ponger.send(PingMessage(text="startup message from ponger..."))
    joinall([pinger, ponger])
