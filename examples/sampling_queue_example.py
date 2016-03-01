import add_import_path
__author__ = 'ceremcem'

from aktos_dcs import *

class Test1(Actor):
    def prepare(self):
        self.msg_queue = SamplingQueue(sample_interval=10)

    def action(self):
        while True:
            msg = self.msg_queue.get()
            print "-----------> frame is shown: ", msg

    def handle_LedPanelMessage(self, msg):
        self.msg_queue.put(msg["message"])
        print "Test1 got message: ", msg["message"]

class Test2(Actor):
    def action(self):
        i = 0
        while True:
            print "Test2 is sending messages with a too high frequency"
            self.send_LedPanelMessage(message="Hello %d" % i)
            i += 1
            sleep(1)


Test2()  # sending too high frequency messages
Test1()  # can not process such high frequency messages, but last message is important.
wait_all()