__author__ = 'ceremcem'

from aktos_dcs import *

class TestMicropython(SerialPortReader):
    def prepare(self):
        print "started reading serial port..."
        print "-------------------------------"
        print self.ser

    def action(self):
        self.start_io_prompt()

    def on_disconnect(self):
        print "\n[[ Device Physically Disconnected... ]]\n"

    def on_connecting(self):
        while True:
            print "\n[[ Waiting for Device to be physically connected... ]]\n"
            sleep(10)

    def on_connect(self):
        print "\n[[ Device Physically Connected... ]]\n"
        sleep(5)
        self.send_cmd("""import network""", 0.5)
        self.send_cmd("""wlan = network.WLAN(network.STA_IF)""", 0.5)
        self.send_cmd("""wlan.active(True)""", 0.5)
        self.send_cmd("""wlan.scan()""", 5)
        self.send_cmd("""wlan.isconnected()""", 0.5)
        self.send_cmd("""wlan.connect("aea", "084DA789BF")""", 10)
        self.send_cmd("""wlan.isconnected()""", 2)
        self.send_cmd("""wlan.isconnected()""", 2)
        self.send_cmd("""wlan.isconnected()""", 2)
        self.send_cmd("""wlan.isconnected()""", 2)



TestMicropython(port="/dev/ttyUSB0", baud=115200)
wait_all()
