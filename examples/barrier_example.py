import add_import_path # only for examples

from aktos_dcs import *

class A(Actor):
    def action(self):
        while True:
            print "asking for temperature"
            self.send_HowHotIsIt()
            sleep(5)

    def handle_ReHowHotIsIt(self, msg):
        print "temperature is: ", msg["temp"]

class Middle(Actor):
    def action(self):
        self.sensor_reply = Barrier()
        self.real_temp = None

    def handle_HowHotIsIt(self, msg):
        print "got temperature question, asking to temp sensor"
        self.send_TemperatureSensor()
        self.sensor_reply.wait_answer()
        print "got real answer: ", self.real_temp
        self.send_ReHowHotIsIt(temp=self.real_temp)

    def handle_TemperatureSensorMessage(self, msg):
        self.real_temp = msg["degree"]
        self.sensor_reply.go()

class TempSensor(Actor):
    def action(self):
        self.i = 0

    def handle_TemperatureSensor(self, msg):
        print "sending simulated (and delayed) sensor message"
        sleep(2)
        self.send_TemperatureSensorMessage(degree=self.i)
        self.i += 1


A() # asks for current temperature
Middle() # gets real measurement from TempSensor, passes that value to A
TempSensor() # measures real temperature
wait_all()