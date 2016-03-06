__author__ = 'ceremcem'

import time
from gevent.lock import BoundedSemaphore
from barrier import Barrier
from gevent import sleep
from gevent.queue import Queue

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
    def __init__(self, sampling_interval=0.033, maxsize=None):
        object.__init__(self)
        self.__queue = Queue(maxsize=maxsize)
        self.buff = SamplingBuffer(sampling_interval=sampling_interval)

    def action(self):
        while True:
            self.__queue.put(self.buff.get())

    def put(self, item):
        self.buff.put(item)

    def get(self):
        return self.__queue.get()


class SamplingBuffer(object):
    def __init__(self, sampling_interval=0, initial_value=None):
        """
        if value is put too fast, `get` method should limit this speed with "sample interval" parameter.

        if value is got too slow, `get` method should return immediately

        """
        self.sampling_interval = sampling_interval
        self.curr_val = initial_value
        self.last_timestamp = 0
        self.put_barrier = Barrier()
        self.fine_tune_last_wait = 0.01  # seconds

    def put(self, value):
        self.curr_val = value
        self.put_barrier.go()

    def get(self):
        while True:
            remaining_time = self.last_timestamp + self.sampling_interval - time.time()
            print "remaining time: ", remaining_time
            if remaining_time <= 0:
                self.put_barrier.wait()
                self.last_timestamp = time.time()
                return self.curr_val
            else:
                if remaining_time > self.fine_tune_last_wait:
                    sleep(remaining_time - self.fine_tune_last_wait)
                else:
                    # try to wait in the last second very
                    sleep(remaining_time/2)


