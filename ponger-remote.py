__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Ponger(Actor):
    def receive(self, msg):
        print "ponger remote got message: ", msg


    def handle_PongMessage(self, msg):
        print "Ponger REMOTE got pong message: ", msg.text, msg.timestamp
        sleep(2)
        self.send(PingMessage(text="Hello pinger, this is ponger REMOTE!"))


if __name__ == "__main__":
    ProxyActor(broker_host="10.0.10.50")
    ponger = Ponger()
    ponger.send(PingMessage(text="startup message from ponger REMOTE..."))
    ponger.join()
