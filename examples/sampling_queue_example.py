from aktos_dcs import *


class Test1(Actor):
    def prepare(self):
        self.sampling_interval = 1
        self.msg_buff = SamplingQueue(sampling_interval=self.sampling_interval)

    def action(self):
        sleep(4)
        while True:
            msg = self.msg_buff.get()
            print "-----------> sample is shown which is got in every %d seconds: " % self.sampling_interval, msg

    def handle_LedPanelMessage(self, msg):
        self.msg_buff.put(msg["message"])


class Test2(Actor):
    def action(self):
        for i in range(20):
            print "Test2 is sending messages (too fast)"
            self.send_LedPanelMessage(message="Hello %d" % i)
            i += 1
            sleep(0.5)


Test2()  # sending too high frequency messages
Test1()  # can not process such high frequency messages, but last message is important.
wait_all()
