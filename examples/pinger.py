import add_import_path # only for examples

from aktos_dcs import *

class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg['text']
        sleep(2)
        self.send({'PongMessage': {'text': "Hello ponger, this is pinger 1!"}})

if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send({'PongMessage': {'text': "Hello ponger, this is STARTUP MESSAGE!"}})

    wait_all()
