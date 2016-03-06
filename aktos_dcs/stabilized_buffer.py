__author__ = 'ceremcem'

from barrier import Barrier

class StabilizedBuffer(object):
    def __init__(self, duration=0):
        object.__init__(self)
        self.duration = duration
        self.curr_val = None
        self.barrier = Barrier()

    def put(self, value):
        self.curr_val = value
        self.barrier.go()

    def get(self):
        while True:
            success = self.barrier.wait(self.duration)
            if not success:
                # barrier is timed out, so there is no new
                # value in this time slot, which means we have
                # a stable value. return this value.
                return self.curr_val

if __name__ == "__main__":
    from gevent_actor import *
    from gevent import sleep

    class Test(Actor):
        def prepare(self):
            # we will get values if values are stable for at least 1 seconds
            self.test_buff = StabilizedBuffer(5)
            self.test_buff2 = StabilizedBuffer(5)

        def action(self):
            while True:
                x = self.test_buff.get()
                print "----SHOULD NEVER GET A VALUE! ---> getting buffer value: ", x

        def action_4(self):
            while True:
                x = self.test_buff2.get()
                print "-------> getting buffer2 value: ", x

        def action_2(self):
            i = 0
            while True:
                print "setting buffer value (too fast):", i
                self.test_buff.put(i)
                i += 1
                sleep(2)

        def action_3(self):
            i = 100
            while True:
                print "setting buffer2 value (slow enough):", i
                self.test_buff2.put(i)
                i += 100
                sleep(6)


    print "Starting test..."
    Test()
    wait_all()