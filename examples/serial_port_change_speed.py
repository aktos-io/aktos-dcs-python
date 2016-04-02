__author__ = 'ceremcem'

from aktos_dcs import *


class TestEsp(SerialPortReader):
    def on_connect(self):
        print ""
        print "[[ Device connected, baudrate: %d ]]" % self.ser.baudrate
        print ""
        if self.ser.baudrate != 115200:
            self.send_cmd("uart.setup(0,115200,8,0,1)")
            sleep(0.1)
            self.ser.baudrate = 115200
            self.ser.close()
        else:
            print "High baudrate: "
            print self.ser

    def on_disconnect(self):
        print ""
        print "[[ Device disconnected... ]]"
        print ""

    def on_connecting(self):
        sleep(1)
        if self.ser.baudrate == 115200:
            self.ser.baudrate = 9600
            self.ser.close()

    def action(self):
        self.start_io_prompt()


TestEsp(port="/dev/ttyUSB0", baud=9600)
wait_all()