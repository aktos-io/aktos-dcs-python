__author__ = 'ceremcem'

from aktos_dcs import Actor, joinall, sleep
from aktos_dcs.Messages import *

from AppMessages2 import *



class TestActor(Actor):
    def handle_TestMessage(self, msg):
        print "received test message: ", msg

    def handle_TestMessage2(self, msg):
        print "received test message 2: ", msg

if __name__ == "__main__":
    test1 = TestActor()
    test2 = TestActor()

    print "test message 1:"
    test1.send(TestMessage(text="this is test 1!"))

    print "test message 2:"
    test1.send(TestMessage2(text="this is test 2!"))

    sleep(1)