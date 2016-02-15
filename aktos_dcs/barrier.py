__author__ = 'ceremcem'


import gevent

class Barrier(object):
    def __init__(self):
        self.barrier_closed = True

    def wait(self):
        self.wait_answer()

    def go(self, msg=None):
        self.answer(msg)

    def wait_answer(self):
        self.barrier_closed = True
        while self.barrier_closed:
            gevent.sleep(0.0001)

    def answer(self, msg=None):
        self.barrier_closed = False

