__author__ = 'ceremcem'


from gevent.queue import Queue


class Barrier(object):
    def __init__(self):
        self.q = Queue()

    def wait_answer(self):
        return self.q.get()

    def answer(self, msg):
        self.q.put(msg)