from aktos_dcs import *


class Foo(Actor):
    def action(self):
        self.send_BarMessage(text="Hello bar, this is startup message from foo!")

    def handle_FooMessage(self, msg):
        print "Foo got FooMessage: ", msg['text']
        sleep(1)
        self.send_BarMessage(text="Hello bar, this is foo!")

if __name__ == "__main__":
    ProxyActor()
    Foo()
    wait_all()