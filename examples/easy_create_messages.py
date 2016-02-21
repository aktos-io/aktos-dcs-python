__author__ = 'ceremcem'
import add_import_path

from aktos_dcs import *

class Test1(Actor):
    def handle_TestMessage(self, msg):
        print "Test1 got message: ", msg


class Test2(Actor):
    def action(self):
        while True:
            #self.send_TestMessage(text='x', mode="y")
            self.send_TestMessage("naber")
            sleep(2)


Test1()
Test2()
wait_all()