from aktos_dcs import * 
from aktos_dcs_lib import * 
import time 

out = 4
inp = 17

GPIOInputActor(pin_name="test_input", pin_number=inp, invert=True)
GPIOOutputActor(pin_name="test_output", pin_number=out)

class Test(Actor): 
    def action(self):
        self.block = Barrier()
        self.input_value = False

        print "starting test..."
        while True: 
            print "setting to true"
            self.set_test_output(True)
            start_time = time.time()
            while self.input_value != True: 
                sleep()
            print "input is true"
            time_diff = time.time() - start_time
            if time_diff > 0.005: 
                print "Time diff: ", time_diff
            self.set_test_output(False)
            sleep(1)

    def set_test_output(self, value):
        self.send({'IoMessage': {'pin_name': 'test_output', 'val': value}})

    def handle_IoMessage(self, msg):
        if msg["pin_name"] == "test_input": 
            self.input_value = msg["val"]


class Notifier(Actor): 
    def action(self): 
        while True: 
            print "test is running...", time.time()
            sleep(10)

Test()
Notifier()
wait_all()
        
