__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Foo(Actor):
    def handle_FooMessage(self, msg):
        print "Foo got FooMessage: ", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(1)
        self.send(BarMessage(text="Hello bar, this is foo from cca!"))

if __name__ == "__main__":
    ProxyActor()
    foo = Foo()
    foo.send(BarMessage(text="startup message from foo from cca..."))

    foo.join()