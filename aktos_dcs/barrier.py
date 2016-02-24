__author__ = 'ceremcem'


import gevent
import time

class Barrier(object):
    def __init__(self):
        self.barrier_closed = True
        self.wait_answer = self.wait
        self.answer = self.go

    def wait(self, timeout=None):
        self.timeout = timeout
        self.start()
        self.barrier_closed = True
        while self.barrier_closed:
            if self.timeout:
                if (self.start_time + self.timeout) < time.time():
                    # timeout!
                    return False
            gevent.sleep(0.0001)

        return True

    def go(self):
        if not self.barrier_closed:
            print "WARNING: BARRIER IS SET TO GO BEFORE IT IS STARTED TO WAIT!!!"
        self.barrier_closed = False

    def start(self):
        self.restart()

    def restart(self):
        self.start_time = time.time()

    def add(self, seconds):
        try:
            self.timeout += seconds
        except:
            self.timeout = seconds
