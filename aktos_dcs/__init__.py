from cca_messages import Message
from gevent_actor import Actor
from gevent_network_actor import ProxyActor
from gevent import sleep, joinall

if __name__ == "__main__":
    ProxyActor()

    class Test(Actor):
        def receive(self, msg):
            print "got message: ", msg

    print "aktos_dcs init!"
    Test().join()