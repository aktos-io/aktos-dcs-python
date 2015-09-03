from messages import *
try:
    from AppMessages import *
except ImportError:
    import info

from gevent_actor import Actor, ActorManager
from gevent_network_actor import ProxyActor
from gevent import sleep, joinall
from wait_all import wait_all

if __name__ == "__main__":
    ProxyActor()

    class Test(Actor):
        def receive(self, msg):
            print "got message: ", msg

    print "aktos_dcs init!"

    wait_all()
