__author__ = 'ceremcem'

import inspect
import gevent
from gevent.queue import Queue, Full, Empty
import time

from gevent_actor import Singleton

class CcaSignalLoop(object):
    __metaclass__ = Singleton
    def __init__(self):
        try:
            assert self.signals
        except:
            self.signals = []

    def register(self, signal):
        self.signals.append(signal)

    def loop_point(self):
        for signal in self.signals:
            signal.val0 = int(signal._val)
            try:
                signal._val = signal.io_queue[-1]
                signal.io_queue = []
            except IndexError:
                pass



class CcaSignal(object):
    def __init__(self, initial_value=0, edge_max_age=0.1):
        self._val = int(initial_value)
        self.val0 = self._val
        self.supervisor = CcaSignalLoop()
        self.supervisor.register(self)
        self.io_queue = []

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self.io_queue.append(value)

    def edge(self):
        return self._val != self.val0

    def r_edge(self):
        return self.val0 < self._val

    def f_edge(self):
        return self.val0 > self._val

def unit_test():
    import time

    a = CcaSignal()

    a.val = 1
    a.val = 0
    for i in range(3):
        print("a.val: %d" % a.val)
        print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
        print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
        print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
        print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
        gevent.sleep(1)

    """
    should print:

    a.val: 0
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    a.val: 0
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    a.val: 0
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')

    """


def unit_test2():
    a = CcaSignal(0)
    a.val = 1
    print(a.r_edge(), a.f_edge())
    print(a.r_edge(), a.f_edge())
    a.val = 0
    print(a.r_edge(), a.f_edge())
    print(a.r_edge(), a.f_edge())

    """
    should print:
    (True, False)
    (True, False)
    (False, True)
    (False, True)
    """

def unit_test3():
    """
    This unit test shows us, any reader can detect edges only once
    """
    a = CcaSignal()
    a.val = 1
    for j in range(2):
        print("------------")
        for i in range(3):
            print(a.r_edge(), a.f_edge())

        print(a.r_edge(), a.f_edge())
        print(a.r_edge(), a.f_edge())
        print(a.r_edge(), a.f_edge())

    """
    should print:
    ------------
    (True, False)
    (False, False)
    (False, False)
    (True, False)
    (True, False)
    (True, False)
    ------------
    (False, False)
    (False, False)
    (False, False)
    (False, False)
    (False, False)
    (False, False)
    """

def unit_test4():
    a = CcaSignal(edge_max_age=2)
    print a.edge_max_age

    def signal_input():
        print("signal is started toggling")
        for i in range(3):
            a.val = 0
            a.val = 1
            gevent.sleep(0)
        print("signal is stable now")

    g_signal_input = gevent.spawn(signal_input)


    def reader():
        print("this is a slow reader")
        for i in range(10):
            print("a.val: %d" % a.val)
            print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
            print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
            print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
            print(a.edge(), a.edge(), a.edge(), a.edge(), a.edge(), a.edge())
            gevent.sleep(1)
        print("slow reader finished")

    g_reader = gevent.spawn(reader)

    gevent.joinall([g_signal_input, g_reader])

    """
    should print:

    signal is started toggling
    this is a slow reader
    a.val: 1
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    signal is stable now
    a.val: 1
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    a.val: 1
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    a.val: 1
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    ('f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge', 'f_edge')
    a.val: 1
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    ('r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge', 'r_edge')
    a.val: 1
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    a.val: 1
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    a.val: 1
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    a.val: 1
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    a.val: 1
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    ('', '', '', '', '', '')
    slow reader finished
    """

if __name__ == "__main__":
    #unit_test()
    #unit_test2()
    #unit_test3()

    """
    a = gevent.spawn(unit_test)
    gevent.sleep(0)
    b = gevent.spawn(unit_test)
    gevent.joinall([a, b])
    """
    #unit_test4()

    output = ""
    def dont_print(x=None):
        global output
        try:
            output += x + "\n"
        except:
            pass
        finally:
            return output

    a = CcaSignal(edge_max_age=100)

    def setter():
        gevent.sleep(0.1)

        a.val = 0
        a.val = 1
        a.val = 0
        a.val = 1

    gevent.spawn(setter)

    dont_print("-"*10)

    def reader():
        for i in range(5):
            dont_print("y: %s" % a.r_edge())
            dont_print("d: %s" % a.f_edge())
            gevent.sleep(1)

    gevent.spawn(reader)

    gevent.sleep(6)

    expected_output = """----------
y: False
d: False
y: True
d: False
y: False
d: True
y: True
d: False
y: False
d: False
"""


    try:
        assert dont_print() == expected_output
        print("tests run ok...")
    except:
        raise
    finally:
        pass



    from cStringIO import StringIO
    import sys

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # blah blah lots of code ...
    print "naber"
    print "iyidir"

    sys.stdout = old_stdout

    # examine mystdout.getvalue()
    import pdb
    pdb.set_trace()
    

