import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(2)
        self.send(PingMessage(text="Hello pinger, this is ponger 1!"))

if __name__ == "__main__":
    ProxyActor()
    #ProxyActor(brokers="192.168.2.119:5012:5013", proxy_brokers="localhost:8012:8013")
    #ProxyActor(brokers="192.168.1.3:5012:5013")
    ponger = Ponger()
    ponger.send(PingMessage(text="startup message from ponger 1..."))

    wait_all()
