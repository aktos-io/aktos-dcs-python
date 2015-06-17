# coding: utf-8
__author__ = 'ceremcem'

import gevent
from cca_messages import *
from gevent_actor import Actor
import zmq.green as zmq
import time


class NetworkActor(Actor):

    def __init__(self, host="localhost", rx_port=5013, tx_port=5012):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.broker_sub = self.context.socket(zmq.SUB)
        self.broker_pub = self.context.socket(zmq.PUB)
        self.publisher = self.context.socket(zmq.PUB)

        self.host = host
        self.rx_port = rx_port
        self.tx_port = tx_port


        self.subscriber.setsockopt(zmq.SUBSCRIBE, '')
        self.broker_sub.setsockopt(zmq.SUBSCRIBE, '')

        # new actor will bind to a random port
        self.port = self.publisher.bind_to_random_port(addr="tcp://*")
        print "this actor's default publish port is: ", self.port

        # peers known so far
        self.peers = [self.port]

        self.rx_addr = "tcp://%s:%d" % (self.host, self.rx_port)
        self.tx_addr = "tcp://%s:%d" % (self.host, self.tx_port)

        self.introduction = "NOK" # not okay, introduce itself

        try:
            self.create_broker(watch=False)
        except:
            print "connecting already created broker"
            # there is a broker_sub binded on rx_port already
            # connect it, send your publisher port, get other's publisher port
            self.broker_pub.connect(self.rx_addr)
            self.broker_sub.connect(self.tx_addr)

            gevent.spawn(self.broker_receiver)

            print "there was a broker, this actor introducing itself"

            gevent.sleep(3)
            for i in range(10):
                print "trial ", i, "..."
                self.broker_pub.send(pack(NetworkActorMessage(peers=self.peers)))
                if self.introduction == "OK":
                    break
                gevent.sleep(0.01)

            print "in case of failure of the broker, watching..."
            gevent.spawn(self.create_broker, watch=True)

        gevent.spawn(self.__receiver__)

        super(NetworkActor, self).__init__()



    def create_broker(self, watch=False):
        while True:
            try:
                rx_addr = "tcp://%s:%d" % ("*", self.rx_port)
                tx_addr = "tcp://%s:%d" % ("*", self.tx_port)

                self.broker_sub.bind(rx_addr)
                self.broker_pub.bind(tx_addr)
                if not watch:
                    gevent.spawn(self.broker_receiver)
                print "this actor created a broker"

                # tell the others about known peers
                while self.introduction != "OK":
                    self.broker_pub.send(pack(NetworkActorMessage(peers=self.peers)))
                    gevent.sleep(0.01)

                break  # quit trying to create a broker
            except Exception as e:
                print e.message
                if not watch:
                    raise
                gevent.sleep(10)  # TODO: decrease this time

            gevent.sleep()

    def broker_receiver(self):
        print "broker receiver called!"
        while True:
            message = self.broker_sub.recv()
            self.call_the_handler(message)


    def handle_NetworkActorMessage(self, msg):

        print "debug: NetworkActorMessage received:", msg.peers

        if self.port in msg.peers:
            self.introduction = "OK"

        for port in msg.peers:
            if port not in self.peers:
                print "discovered another actor binded to port %d" % port
                self.subscriber.connect("tcp://localhost:%d" % port)
                self.peers.append(port)
                print "subscriber is connected to the new actor"

                print "msg.peers: ", msg.peers

        if set(msg.peers) != set(self.peers):
            print "informing others about known peers so far"
            self.broker_pub.send(pack(NetworkActorMessage(peers=self.peers)))

    def network_receive(self, msg):
        pass

    def __receiver__(self):
        try:
            #print "started to receive"
            while True:
                message = self.subscriber.recv()
                ###print "got message:", message
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

