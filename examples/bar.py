import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Bar(Actor):
    def handle_BarMessage(self, msg):
        msg = msg_body(msg)
        print "Bar got BarMessage: ", msg['text']
        sleep(1)
        self.send({'FooMessage': {'text': "Hello foo, this is bar from cca!"}})

if __name__ == "__main__":
    ProxyActor()
    bar = Bar()
    bar.send({'FooMessage': {'text': "startup message from bar from cca..."}})

    wait_all()