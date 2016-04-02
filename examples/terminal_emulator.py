__author__ = 'ceremcem'

from aktos_dcs import *

class TerminalEmulator(SerialPortReader):
    def prepare(self):
        print "started terminal emulator..."
        print "-----------------------------"
        print self.ser

    def action(self):
        self.start_io_prompt()

    def on_disconnect(self):
        print ""
        print "[[ Device Physically Disconnected... ]]"
        print ""

    def on_connecting(self):
        print ""
        while True:
            print "[[ Waiting for Device to be physically connected... ]]"
            sleep(5)

    def on_connect(self):
        print ""
        print "[[ Device Physically Connected... ]]"
        print ""

TerminalEmulator(port="/dev/ttyUSB0", baud=115200)
wait_all()
