__author__ = 'ceremcem'

from aktos_dcs import *

class Bar(Actor):
    def handle_BarMessage(self, msg):
        print "Bar got BarMessage: ", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(1)
        self.send(FooMessage(text="Hello foo, this is bar from cca!"))

if __name__ == "__main__":
    ProxyActor()
    bar = Bar()
    bar.send(FooMessage(text="startup message from bar from cca..."))

    bar.join()