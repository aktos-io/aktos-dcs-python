import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class TestActor(Actor):
    def handle_TestMessage(self, msg):
        print "received test message: ", msg

if __name__ == "__main__":
    ProxyActor()
    test1 = TestActor()


    while True:
        print "test message 1:"
        test1.send(TestMessage(text="this is test 1!"))
        sleep(3)

    wait_all()