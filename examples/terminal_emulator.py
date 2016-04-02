__author__ = 'ceremcem'

from aktos_dcs import *

class TerminalEmulator(SerialPortReader):
    def prepare(self):
        print "started terminal emulator..."
        print "-----------------------------"
        print self.ser

    def action(self):
        self.start_io_prompt()

    def send_cmd(self, cmd, s=0.5):
        self.serial_write(cmd + self.line_endings)
        sleep(0.1)

    def on_disconnect(self):
        print "\n[[ Device Physically Disconnected... ]]\n"

    def on_connecting(self):
        while True:
            print "\n[[ Waiting for Device to be physically connected... ]]\n"
            sleep(1)

    def on_connect(self):
        print "\n[[ Device Physically Connected... ]]\n"

        # send any command with `self.send_cmd`
        ###self.send_cmd("hello")

TerminalEmulator(port="/dev/ttyUSB0", baud=115200)
wait_all()
