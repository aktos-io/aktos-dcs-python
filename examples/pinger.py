from aktos_dcs import *


class Pinger(Actor):
    def action(self):
        self.send_PongMessage(text="Hello ponger, this is STARTUP MESSAGE!")

    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg['text']
        sleep(2)
        self.send_PongMessage(text="Hello ponger, this is pinger1!")

if __name__ == "__main__":
    ProxyActor()
    Pinger()
    wait_all()
