__author__ = 'ceremcem'

import time
from gevent.lock import BoundedSemaphore
from barrier import Barrier
from gevent import sleep

class SamplingQueue(object):
    """
    FIFO queue with a sampling interval

    if an item is put this queue at a higher frequency that sample_interval
    allows, the last value in this queue is discarded and replaced with new
    value.

    if a value is requested from this queue and it is not available,
    then `get()` method blocks execution.

    if values are requested too quick, then `get()` method blocks
    execution until a sample_interval elapses, and returns last item.
    """
    def __init__(self, sample_interval=0.033, size=0):
        object.__init__(self)
        self.__queue = []
        self.last_put_time = 0
        self.last_get_time = None
        self.sample_interval = sample_interval  # seconds
        self.lock = BoundedSemaphore()
        self.barrier = Barrier()
        self.warnings = False
        self.size = size

    def put(self, item):
        self.lock.acquire()
        if ((time.time() >= (self.last_put_time + self.sample_interval)) or
                (len(self.__queue) == 0)):

            if self.size > 0 and len(self.__queue) < self.size:
                self.__queue.append(item)
                self.last_put_time = time.time()
            else:
                self.__queue[-1] = item

            if self.barrier.is_waiting():
                self.barrier.go()
        else:
            if self.warnings:
                print "Warning: too new sample, discarding old one..."
            self.__queue[-1] = item
        self.lock.release()


    def get(self):
        while True:
            try:
                if self.last_get_time:
                    wait_interval = (self.last_get_time + self.sample_interval
                        - time.time())
                    if wait_interval > 0:
                        sleep(wait_interval)
                x = self.__queue.pop(1)
                self.last_get_time = time.time()
                return x
            except IndexError:
                self.barrier.wait()
