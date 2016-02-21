__author__ = 'ceremcem'


import gevent

class Barrier(object):
    def __init__(self):
        self.barrier_closed = True

    def wait_answer(self, timeout=None):
        x = self.wait(timeout)
        return x

    def go(self):
        self.answer()

    def wait(self, timeout=None):
        t = gevent.Timeout(timeout)
        success = False
        try:
            t.start()
            self.barrier_closed = True
            while self.barrier_closed:
                gevent.sleep(0.0001)
            success = True
        except:
            success = False
        finally:
            t.cancel()

        return success

    def answer(self):
        self.barrier_closed = False

