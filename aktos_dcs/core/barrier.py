__author__ = 'ceremcem'


import gevent
from gevent.event import Event
import time

class Barrier(object):
    def __init__(self, warning=False):
        # aliases for functions
        self.wait_answer = self.wait
        self.answer = self.go

        self.go_timestamp = 0
        self.tolerance_before_wait = 0.01  # seconds
        self.warning = False
        self.barrier_event = Event()

    def wait(self, timeout=None):
        """
        if self.go_timestamp + self.tolerance_before_wait >= time.time():
            if self.warning:
                print "WARNING: Go signal has been gathered %f seconds before wait, but continuing anyway.." % (
                    time.time() - self.go_timestamp
                )
            return True
        else:
            if self.warning:
                print "WARNING: Go signal has been gathered too long before wait, not continuing!"
        self.start()
        """
        #print "starting event wait, timeout: ", timeout
        success = self.barrier_event.wait(timeout)
        #print "finished event wait, success: ", success
        self.barrier_event.clear()
        return success

    def go(self):
        self.go_timestamp = time.time()
        self.barrier_event.set()

    def start(self):
        self.start_time = time.time()

    def restart(self):
        self.start()

    def is_waiting(self):
        return not self.barrier_event.ready()
