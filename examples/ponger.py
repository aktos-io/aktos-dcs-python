from aktos_dcs import *


class Ponger(Actor):
    def action(self):
        self.send_PingMessage(text="Hello pinger, this is STARTUP MESSAGE!")

    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg['text']
        sleep(2)
        self.send_PingMessage(text="Hello pinger, this is ponger 1!")

if __name__ == "__main__":
    ProxyActor(brokers="192.168.2.161:5012:5013")
    Ponger()
    wait_all()
