import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class TestActor(Actor):
    def handle_TestMessage(self, msg):
        print "received test message: ", msg

if __name__ == "__main__":
    ProxyActor()
    test1 = TestActor()

    wait_all()
