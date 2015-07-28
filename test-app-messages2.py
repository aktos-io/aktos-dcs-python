__author__ = 'ceremcem'

from aktos_dcs import *

from aktos_dcs.cca_messages import test
test()

class TestActor(Actor):
    def handle_TestMessage(self, msg):
        print "received test message: ", msg

if __name__ == "__main__":
    ProxyActor()
    test1 = TestActor()
    test1.join()
