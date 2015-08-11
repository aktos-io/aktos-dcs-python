__author__ = 'ceremcem'

import inspect
import gevent
import gevent.queue
import time

from gevent_actor import Singleton

class CcaSignalLoop(object):
    __metaclass__ = Singleton



class CcaSignal(object):
    """
    for rising edge and falling edge;
    every reader has a queue
    every event is put in the reader's queue
    when reader ask for status, this is got from the reader's queue
    """

    def __init__(self, initial_value=0, edge_max_age=2.0):
        self.__val = bool(initial_value)
        self.__val0 = self.__val # previous value
        self.__usage_points__ = {} # usage_id, edge_queue
        self.edge_max_age = edge_max_age

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, value):
        new_val = bool(value)
        if new_val != self.__val:
            self.__val0 = self.__val
            self.__val = new_val

            if not self.__val0 and self.__val:
                edge = self.__r_edge_data()
            else:
                edge = self.__f_edge_data()

            for queue in self.__usage_points__.values():

                queue.put(edge)

    @property
    def pval(self):
        return self.__val0

    f_edge_name = "f_edge"
    r_edge_name = "r_edge"

    def __f_edge_data(self):
        return self.__edge_data(self.f_edge_name)

    def __r_edge_data(self):
        return self.__edge_data(self.r_edge_name)

    def __edge_data(self, edge_name):
        return [edge_name, time.time()]

    def _edge(self, usage_id):
        # TODO: if first reader came again, change should loose its importance, thus return "" for everyone
        if usage_id not in self.__usage_points__.keys():
            q = gevent.queue.Queue()
            if self.pval and not self.val:
                q.put(self.__f_edge_data())
            elif not self.pval and self.val:
                q.put(self.__r_edge_data())

            self.__usage_points__[usage_id] = q

        try:
            while True:
                curr_edge, event_date = self.__usage_points__[usage_id].get_nowait()
                if time.time() - event_date > self.edge_max_age:
                    print("DEBUG: CcaSignal: Too old value!")
                    curr_edge = ""
                else:
                    break
                gevent.sleep(0)
        except:
            curr_edge = ""

        return curr_edge


    def edge(self):
        """
        do not move following part of code
        to another method of this class
        """
        f = inspect.currentframe().f_back
        greenlet_id = id(gevent.getcurrent())
        caller_id = ".".join(map(str, [f.f_lineno, f.f_lasti, greenlet_id]))
        return self._edge(caller_id)

    def r_edge(self):
        """
        do not move following part of code
        to another method of this class
        """
        f = inspect.currentframe().f_back
        greenlet_id = id(gevent.getcurrent())
        caller_id = ".".join(map(str, [f.f_lineno, f.f_lasti, greenlet_id]))
        return self._edge(caller_id) == self.r_edge_name

    def f_edge(self):
        """
        do not move following part of code
        to another method of this class
        """
        f = inspect.currentframe().f_back
        greenlet_id = id(gevent.getcurrent())
        caller_id = ".".join(map(str, [f.f_lineno, f.f_lasti, greenlet_id]))
        return self._edge(caller_id) == self.f_edge_name


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
    

