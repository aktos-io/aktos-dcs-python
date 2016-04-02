__author__ = 'ceremcem'

from aktos_dcs import *

import sys

class TestMicropython(SerialPortReader):
    def prepare(self):
        print "started reading serial port..."
        print "-------------------------------"
        print self.ser

    def send_cmd(self, cmd, s=0.5):
        self.serial_write(cmd + "\r\n")
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
        sys.stdout.write(data)

TestMicropython(port="/dev/ttyUSB0", baud=115200)
wait_all()
