__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg.msg_id, (time.time() - msg.timestamp), msg.debug
        sleep(2)
        self.send(PingMessage(text="Hello pinger, this is ponger 1!"))

if __name__ == "__main__":
    p = ProxyActor()
    ponger = Ponger()
    while True:
        ponger.send(PingMessage(text="startup message from ponger cca..."))
        sleep(1)

    ponger.join()
