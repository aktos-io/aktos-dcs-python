import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Bar(Actor):
    def action(self):
        self.send_FooMessage(text="Hello foo, this is STARTUP MESSAGE!")

    def handle_BarMessage(self, msg):
        print "Bar got BarMessage: ", msg['text']
        sleep(1)
        self.send_FooMessage(text="Hello foo, this is bar!")

if __name__ == "__main__":
    ProxyActor()
    Bar()
    wait_all()