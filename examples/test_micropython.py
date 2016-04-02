__author__ = 'ceremcem'

from aktos_dcs import *

import sys

class TestMicropython(SerialPortReader):
    def prepare(self):
        print "started reading serial port..."
        print "-------------------------------"
        print self.ser
        self.last_input = None
        self.line_endings = "\r\n"

    def send_cmd(self, cmd, s=0.5):
        self.serial_write(cmd + self.line_endings)
        sleep(s)

    def on_disconnect(self):
        print "\n[[ Device Physically Disconnected... ]]\n"

    def on_connecting(self):
        while True:
            print "\n[[ Waiting for Device to be physically connected... ]]\n"
            sleep(1)

    def on_connect(self):
        print "\n[[ Device Physically Connected... ]]\n"
        sleep(5)
        self.send_cmd("""import network""")
        self.send_cmd("""wlan = network.WLAN(network.STA_IF)""")
        self.send_cmd("""wlan.active(True)""")
        self.send_cmd("""wlan.scan()""", 5)
        self.send_cmd("""wlan.isconnected()""")
        self.send_cmd("""wlan.connect("aea", "084DA789BF")""", 10)
        self.send_cmd("""wlan.isconnected()""")
        self.send_cmd("""wlan.isconnected()""", 2)
        self.send_cmd("""wlan.isconnected()""", 2)
        self.send_cmd("""wlan.isconnected()""", 2)

    def serial_read(self, data):
        #print 'Serial Port Received: ', data
        echo_index = 0
        if self.last_input is not None:
            if self.last_input[-1] == "\n":
                self.last_input = self.last_input[:-1]  # remove \n char

            echo_index = data.find(self.last_input)
            if echo_index > -1:
                echo_index += len(self.last_input)
                echo_index += len(self.line_endings)  # remove \r\n at the end
            self.last_input = None
        clear_data = data[echo_index:]
        sys.stdout.write(clear_data)
        sys.stdout.flush()

    def action2(self):
        while True:
            self.last_input = raw_input()
            self.send_cmd(self.last_input)
            sleep(0)


TestMicropython(port="/dev/ttyUSB0", baud=115200)
wait_all()
