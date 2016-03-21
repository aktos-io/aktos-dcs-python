from aktos_dcs import *

"""
This example is not working due to slow loops and fast io messages!
assert False
"""

class Test(Actor):
    def prepare(self):
        self.input_1 = CcaSignal()

    def plc_loop(self):
        if self.input_1.r_edge:
            print "input 1 rising edge detected in plc_loop!"

    def plc_loop2(self):
        if self.input_1.r_edge:
            print "input 1 rising edge detected in plc_loop2!"


    def handle_IoMessage(self, msg):
        if msg["pin_name"] == "input_1":
            self.input_1.val = msg["val"]
            print "handled IoMessage:", msg["val"]


class TestIo(Actor):
    def prepare(self):
        self.curr_val = True

    def action(self):
        while True:
            self.send_IoMessage(pin_name="input_1", val=self.curr_val)
            sleep(1)

    def action2(self):
        while True:
            self.curr_val = not self.curr_val
            sleep(5)



Test()
TestIo()
wait_all()