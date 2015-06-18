__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Pinger(Actor):
    def receive(self, msg):
        print "pinger remote got message: ", msg

    def handle_PingMessage(self, msg):
        print "Pinger REMOTE got ping message: ", msg.text, msg.timestamp
        sleep(2)
        self.send(PongMessage(text="Hello ponger, this is pinger REMOTE!"))


if __name__ == "__main__":
    ProxyActor(broker_host="192.168.1.87")
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger REMOTE..."))
    joinall([pinger])
