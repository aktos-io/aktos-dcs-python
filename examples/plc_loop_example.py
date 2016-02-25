import add_import_path # only for examples
__author__ = 'ceremcem'
from aktos_dcs import *

class Test(Actor):
    def plc_loop(self):
        print "hello from plc loop 1"
        sleep(2)
        print "how are you from plc loop 1"
        sleep(3)

    def plc_loop2(self):
        print "hello from plc loop 2"
        sleep(2)
        print "how are you from plc loop 2"
        sleep(3)

    def action(self):
        print "hello from action"
        sleep(2)
        print "how are you from action"
        sleep(3)

    def action_2(self):
        print "hello from action 2"





Test()
wait_all()