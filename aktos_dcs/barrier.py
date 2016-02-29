__author__ = 'ceremcem'


import gevent
from gevent.event import Event
import time

class Barrier(object):
    def __init__(self, warning=False):
        self.barrier_closed = True
        self.wait_answer = self.wait
        self.answer = self.go
        self.go_timestamp = 0
        self.tolerance_before_wait = 0.01  # seconds
        self.warning = warning
        self.barrier_event = Event()

    def wait(self, timeout=None):
        self.timeout = timeout
        self.start()

        if self.go_timestamp + self.tolerance_before_wait >= time.time():
            if self.warning:
                print "WARNING: Go signal has been gathered %f seconds before wait, but continuing anyway.." % (
                    time.time() - self.go_timestamp
                )
            return True
        else:
            if self.warning:
                print "WARNING: Go signal has been gathered too long before wait, not continuing!"

        self.barrier_closed = True
        while True:
            if self.timeout:
                if (self.start_time + self.timeout) < time.time():
                    # timeout!
                    return False
            if not self.barrier_closed:
                break

            gevent.sleep(0.0001)

        return True

    def go(self):
        if not self.barrier_closed:
            if self.warning:
                print "WARNING: BARRIER IS SET TO GO BEFORE IT IS STARTED TO WAIT!!!"
        self.barrier_closed = False
        self.go_timestamp = time.time()

    def start(self):
        self.restart()

    def restart(self):
        self.start_time = time.time()

    def add(self, seconds):
        try:
            self.timeout += seconds
        except:
            self.timeout = seconds
