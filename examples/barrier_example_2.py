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
        #sleep(1)
        print "setting again to 3 seconds, will timeout", self.time_diff()
        success = self.b.wait(3)
        print "wait ends", self.time_diff()


    def action2(self):
        sleep(2)
        print "after 2 seconds, go! signal is emitted: ", self.time_diff()
        self.b.go()

    def action3(self):
        x = Barrier()
        print "Barrier X has been opened before close"
        x.go()
        x.wait()
        print "Barrier X continues..."
"""
Expected output:

Barrier X has been opened before close
Barrier X continues...
after 2 seconds, go! signal is emitted:  2.00133919716
wait ends 2.00144314766
setting again to 3 seconds, will timeout 2.00145411491
wait ends 5.00199604034


"""

Test()
wait_all()

