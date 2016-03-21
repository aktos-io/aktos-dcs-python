from aktos_dcs import *


class Test1(Actor):
    def handle_TestMessage(self, msg):
        print "Test1 got message: ", msg["text"], msg["mode"]


class Test2(Actor):
    def action(self):
        while True:
            self.send_TestMessage(text="x", mode="y")
            sleep(2)


Test1()
Test2()
wait_all()