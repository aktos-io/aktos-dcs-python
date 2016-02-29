from messages import *
from gevent_actor import Actor, ActorManager
from gevent_network_actor import ProxyActor
from gevent import sleep, joinall
from wait_all import wait_all
from barrier import *
from cca_signal import CcaSignal, CcaSignalLoop

if __name__ == "__main__":
    ProxyActor()

    class Test(Actor):
        def receive(self, msg):
            print "got message: ", msg

    print "aktos_dcs init!"

    wait_all()
