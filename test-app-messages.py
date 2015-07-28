__author__ = 'ceremcem'

from aktos_dcs import *

from aktos_dcs.cca_messages import test
test()

class TestActor(Actor):
    def handle_TestMessage(self, msg):
        print "received test message: ", msg

    def handle_TestMessage2(self, msg):
        print "received test message 2: ", msg


if __name__ == "__main__":

    ProxyActor()

    test1 = TestActor()
    test2 = TestActor()

    print "test message 1:"
    test1.send(TestMessage(text="this is test 1!"))

    print "test message 2:"
    test1.send(TestMessage2(text="this is test 2!"))

    while True:
        test1.send(Message(t="naber"))
        test1.send(TestMessage(text="this is test 1!"))
        sleep(3)
    test1.join()