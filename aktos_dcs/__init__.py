from cca_messages import *
try:
    from AppMessages import *
except ImportError:
    print "hint: "
    print "hint: You may define App specific messages "
    print "hint: in AppMessages.py"
    print "hint: "

from gevent_actor import Actor
from gevent_network_actor import ProxyActor
from gevent import sleep, joinall
from cca_signal import CcaSignal

if __name__ == "__main__":
    ProxyActor()

    class Test(Actor):
        def receive(self, msg):
            print "got message: ", msg

    print "aktos_dcs init!"
    Test().join()