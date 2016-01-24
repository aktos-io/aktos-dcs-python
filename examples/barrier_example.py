import add_import_path # only for examples

from aktos_dcs import *

class A(Actor):
    def action(self):
        while True:
            print "asking for temperature"
            self.send({'HowHotIsIt': {}})
            sleep(5)

    def handle_ReHowHotIsIt(self, msg):
        print "temperature is: ", msg["temp"]

class Middle(Actor):
    def action(self):
        self.sensor_reply = Barrier()

    def handle_HowHotIsIt(self, msg):
        print "got temperature question, asking to temp sensor"
        self.send({'TemperatureSensor': {}})
        reply = self.sensor_reply.wait_answer()
        print "got real answer: ", reply["degree"]
        self.send({'ReHowHotIsIt': {'temp': reply['degree']}})

    def handle_TemperatureSensorMessage(self, msg):
        self.sensor_reply.answer(msg)

class TempSensor(Actor):
    def action(self):
        self.i = 0

    def handle_TemperatureSensor(self, msg):
        print "sending simulated (and delayed) sensor message"
        sleep(2)
        self.send({'TemperatureSensorMessage': {'degree': self.i}})
        self.i += 1


A()
Middle()
TempSensor()
wait_all()