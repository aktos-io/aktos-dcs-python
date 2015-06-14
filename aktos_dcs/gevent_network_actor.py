# coding: utf-8
__author__ = 'ceremcem'

import gevent
from cca_messages import *
from gevent_actor import Actor
import zmq.green as zmq
import time


class NetworkActor(Actor):

    def __init__(self, host="localhost", port=5012):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.introducer = self.context.socket(zmq.PUB)
        self.publisher = self.context.socket(zmq.PUB)

        self.host = host
        self.default_port = port

        # everyone listens to the introducer
        self.subscriber.connect("tcp://localhost:%d" % self.default_port)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, '')
        gevent.spawn(self.__receiver__)

        # new object will bind to a random port
        self.port = self.publisher.bind_to_random_port(addr="tcp://*")

        # peers known so far
        self.peers = [self.port]

        self.discover()

        self.g_syncer = None
        super(NetworkActor, self).__init__()



    def discover(self):
        # introduce itself to others
        self.introduction_is_successfull = False
        while not self.introduction_is_successfull:
            try:
                self.introducer.bind("tcp://*:%d" % self.default_port)
                #print "started to listen!"
                while True:
                    self.introducer.send(pack(NetworkActorMessage(peers=self.peers)))
                    if self.introduction_is_successfull:
                        break
                    gevent.sleep(1)
                self.introducer.close()
            except:
                pass
            gevent.sleep()


    def handle_NetworkActorMessage(self, msg):
        if msg.peers[0] == self.port:
            print "this actor successfully introduced itself"
            self.introduction_is_successfull = True
        else:
            for port in msg.peers:
                if port not in self.peers:
                    print "discovered another actor binded to port %d" % port
                    self.subscriber.connect("tcp://localhost:%d" % port)
                    self.peers.append(port)
                    print "subscriber is connected to the new actor"

                    print "msg.peers: ", msg.peers

        if msg.broadcasting:
            try:
                print "killing broadcaster"
                self.g_syncer.kill()
            except:
                pass

        if not self.g_syncer:
            if set(msg.peers) != set(self.peers):
                print "synchronizing peers"
                self.g_syncer = gevent.spawn(self.__syncer__)

    def __syncer__(self):
        try:
            while True:
                try:
                    #print "started sync!"
                    self.introducer = self.context.socket(zmq.PUB)
                    self.introducer.bind("tcp://*:%d" % self.default_port)
                    while True:
                        self.introducer.send(pack(NetworkActorMessage(peers=self.peers, broadcasting=True)))
                        gevent.sleep(1)
                    self.introducer.close()
                    #print "killing itself!"
                    gevent.getcurrent().kill()
                except Exception as e:
                    #print "syncer exception:" + e.message
                    pass

                gevent.sleep(0.1)
        except:
            #print "syncer killed??"
            self.introducer.close()

    def network_receive(self, msg):
        pass

    def __receiver__(self):
        try:
            #print "started to receive"
            while True:
                message = self.subscriber.recv()
                self.call_the_handler(message)
                gevent.sleep(0)
        finally:
            self.subscriber.close()

    def network_send(self, msg):
        try:
            msg.sender = self.actor_id
            msg = pack(msg)
        except:
            pass
        self.publisher.send(msg)


    def call_the_handler(self, message):
        try:
            m = unpack(message)
        except Exception as e:
            #print "exception in call_the_handler:", e.message
            m = message

        if type(m) != type(NetworkActorMessage()):
            #self.receive(message)
            self.network_receive(message)

        try:
            if isinstance(m, Message):
                handler_func = "handle_" + m.__class__.__name__
                getattr(self, handler_func)(m)
        except AttributeError:
            pass


class ProxyActor(NetworkActor):
    def network_receive(self, msg):
        #print "proxy received network message: ", msg
        self.send(msg)

    def receive(self, msg):
        #print "proxy (id: %d) received msg: id: %d" % (id(self), msg.sender )
        self.network_send(msg)


if __name__ == "__main__":

    class TestNetworkActor(NetworkActor):

        def handle_IoMessage(self, msg):
            print "gevent network actor received: ", msg.nereden

    a = TestNetworkActor()

    for i in range(1000):
        print "sending: this is gevent network actor"
        a.network_send("this is gevent network actor")
        gevent.sleep(10)

    gevent.joinall([a])