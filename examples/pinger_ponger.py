import add_import_path # only for examples
__author__ = 'ceremcem'
from aktos_dcs import *

class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Pong got pong message:", msg['text']
        sleep(2)
        self.send_PingMessage(text="Hello pinger")


class Pinger(Actor):
    def action(self):
        print "pinger is sending startup message..."
        sleep(1)
        self.send_PongMessage(text="Hello ponger, this is startup message!")

    def handle_PingMessage(self, msg):
        print "Ping got ping message: ", msg['text']
        sleep(2)
        self.send_PongMessage(text="Hello ponger!")

if __name__ == "__main__":
    print "lan..."
    Ponger()
    Pinger()
    wait_all()