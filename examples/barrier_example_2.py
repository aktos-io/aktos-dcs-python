import add_import_path # only for examples

from aktos_dcs import *
import time

class Test(Actor):
    def prepare(self):
        self.start_time = time.time()

    def time_diff(self):
        return time.time() - self.start_time

    def action(self):
        self.b = Barrier()

        print "waiting forever"
        success = self.b.wait()
        print "wait ends", self.time_diff()
        print "setting again: 3 seconds", self.time_diff()
        success = self.b.wait(3)
        print "wait ends", self.time_diff()


    def action2(self):
        sleep(2)
        print "adding 5 seconds to timeout", self.time_diff()
        self.b.add(5)
        sleep(5)
        print "restarting...", self.time_diff()
        self.b.restart()


    def action3(self):
        x = Barrier()
        print "Barrier X has been opened before close"
        x.go()
        x.wait()
        print "Barrier X continues..."
"""
Expected output:

waiting forever
adding 5 seconds to timeout 2.00101590157
wait ends 5.00072097778
setting again: 3 seconds 5.00075697899
restarting... 7.00221204758
wait ends 10.0028839111

"""

Test()
wait_all()

