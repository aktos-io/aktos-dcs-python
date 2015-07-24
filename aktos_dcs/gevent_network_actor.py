# coding: utf-8
__author__ = 'ceremcem'

import gevent
from cca_messages import *
from gevent_actor import Actor
import zmq.green as zmq

from pprint import pprint

if zmq.zmq_version_info()[0] < 4:
    raise Exception("libzmq version should be >= 4.x")

import pdb

class ProxyActor(Actor):

    def __init__(self, my_ip="", broker_conn="192.168.2.55:8012:8013, localhost:9012:9013", rx_port=5012, tx_port=5013):
        #super(ProxyActor, self).__init__()
        Actor.__init__(self)
        print "proxy actor created with id: ", self.actor_id


        self.broker_conn = broker_conn
        self.my_ip = my_ip

        self.rx_port = rx_port
        self.tx_port = tx_port

        self.context = zmq.Context()

        # server_link:
        #   inner messages forwarded to server_pub
        #   server_sub forwards to actor manager
        self.server_sub = self.context.socket(zmq.SUB)
        self.server_pub = self.context.socket(zmq.PUB)

        # client_link:
        #   inner messages forwarded to client_pub
        #   client_sub forwards to actor manager
        self.client_sub = self.context.socket(zmq.SUB)
        self.client_pub = self.context.socket(zmq.PUB)


        # broker_link:
        #   this is address broker. others connect to
        #   this link and exchange known publisher's
        #   address+port information (phone book)
        self.broker_sub = self.context.socket(zmq.SUB)
        self.broker_pub = self.context.socket(zmq.PUB)


        # proxy_link:
        #   forwards messages to the other processes
        #   which the client does not have access.
        self.proxy_sub = self.context.socket(zmq.SUB)
        self.proxy_pub = self.context.socket(zmq.PUB)

        self.__subscribers__ = [self.server_sub,
                           self.client_sub,
                           self.broker_sub,
                           self.proxy_sub]

        self.__publishers__ = [self.server_pub,
                           self.client_pub,
                           self.broker_pub,
                           self.proxy_pub]


        for s in self.__subscribers__:
            s.setsockopt(zmq.SUBSCRIBE, '')

        for p in self.__publishers__:
            p.setsockopt(zmq.LINGER, 0)
            p.setsockopt(zmq.SNDHWM, 2)
            p.setsockopt(zmq.SNDTIMEO, 0)


        # spawn the receivers
        __receivers__ = [self.server_sub_receiver,
                         self.client_sub_receiver,
                         self.broker_sub_receiver,
                         self.proxy_sub_receiver]

        for r in __receivers__:
            gevent.spawn(r)


        # server_pub will serve on a random port
        self.server_pub_port = self.server_pub.bind_to_random_port(addr="tcp://*")
        self.server_sub_port = self.server_sub.bind_to_random_port(addr="tcp://*")
        print "this actor's server ports are: ", self.server_sub_port, self.server_pub_port

        # server_pub will serve on a random port
        self.proxy_pub_port = self.proxy_pub.bind_to_random_port(addr="tcp://*")
        self.proxy_sub_port = self.proxy_sub.bind_to_random_port(addr="tcp://*")
        print "this actor's proxy ports are: ", self.proxy_sub_port, self.proxy_pub_port


        """
        self.contact_list = {
            '192.168.2.10': [
                's: 111, 222; p: 333, 444',
                's: 111, 222; p: 333, 444',
                's: 111, 222; p: 333, 444',
            ],
            '192.168.2.50': [],
            }
        """
        self.this_contact = dict()
        self.this_contact[self.my_ip] = ["s: %d, %d; p: %d, %d" % (
            self.server_sub_port, self.server_pub_port,
            self.proxy_sub_port, self.proxy_pub_port
        )]

        self.introduction_msg = ProxyActorMessage(new_entry=self.this_contact)

        self.contact_list = dict(self.this_contact)

        # create or try to create address broker
        self.this_is_the_broker = False
        try:
            self.create_broker(watch=False)
            self.sync_contacts()
        except:
            gevent.spawn(self.create_broker, watch=True)
            self.sync_contacts()



    def sync_contacts(self):
        # go and get other processes' address information
        # connect their server_pub port with your client_sub port

        print "sync contacts..."
        print "this contact: ", self.this_contact

        if not self.this_is_the_broker:
            self.client_pub.connect("tcp://%s:%d" % ("localhost", self.rx_port))
            self.client_sub.connect("tcp://%s:%d" % ("localhost", self.tx_port))

            gevent.sleep(1)
            print "sending introduction msg..."
            self.client_send(self.introduction_msg)


    #TODO: rename client_send to handshake_send or something...
    def client_send(self, msg):
        msg.sender = self.actor_id
        #self.client_pub.send(pack(msg))
        self.propogate_msg_to_others(msg)

    def create_broker(self, watch=False):
        while True:
            try:
                rx_addr = "tcp://%s:%d" % ("*", self.rx_port)
                tx_addr = "tcp://%s:%d" % ("*", self.tx_port)

                self.broker_sub.bind(rx_addr)
                self.broker_pub.bind(tx_addr)

                print "this actor created a broker"
                self.this_is_the_broker = True
                break  # quit trying to create a broker
            except Exception as e:
                if not watch:
                    raise
                gevent.sleep(1)  # TODO: decrease this time

            gevent.sleep()


    def propogate_msg_to_others(self, msg):
        json_msg = pack(msg)
        self.server_pub.send(json_msg)
        self.client_pub.send(json_msg)
        if self.this_is_the_broker:
            self.broker_pub.send(json_msg)

    def receive(self, msg):
        msg.proxied_by.append(self.actor_id)
        self.propogate_msg_to_others(msg)

    def handle_ProxyActorMessage(self, msg):
        print "debug: ProxyActorMessage received", pack(msg)
        if msg.new_entry:
            print "found new entry, adding current contact list..."
            for k, v in msg.new_entry.iteritems():
                for process in v:
                    self.contact_list[k].append(process)

            #pdb.set_trace()
            self.client_send(ProxyActorMessage(
                contact_list=self.contact_list,
                reply_to=msg.msg_id))

            print "merged contact list: "
            pprint(self.contact_list)

        if msg.contact_list:
            print "received update of contact list, updating current..."
            if msg.reply_to == self.introduction_msg.msg_id:
                # this message is in response to the introduction
                # message. connect the processes listed in contact_list
                my_ports = self.this_contact[self.my_ip]
                for k, v in msg.contact_list.iteritems():
                    for ports in v:
                        if k != self.my_ip or my_ports != ports:
                            # other than this process
                            print "will connect to: ", ports

            # simply update the contact list
            self.contact_list = msg.contact_list

            print "replaced contact list: "
            pprint(self.contact_list)

    def server_sub_receiver(self):
        while True:
            msg = self.server_sub.recv()
            self.send_to_inner_actors(msg)
            gevent.sleep()

    def client_sub_receiver(self):
        while True:
            msg = self.client_sub.recv()
            print "this is client_sub_receiver: ", msg
            self.send_to_inner_actors(msg)
            gevent.sleep()

    def broker_sub_receiver(self):
        while True:
            msg = self.broker_sub.recv()
            self.send_to_inner_actors(msg)
            gevent.sleep()

    def proxy_sub_receiver(self):
        while True:
            msg = self.proxy_sub.recv()
            self.send_to_inner_actors(msg)

            m = unpack(msg)
            m.proxied_by.append(self.actor_id)
            mp = pack(msg)
            self.propogate_msg_to_others(mp)
            gevent.sleep()

    def send_to_inner_actors(self, msg):
        m = self.filter_network_msg(msg)
        if m:
            # do not modify msg.sender information
            m.proxied_by.append(self.actor_id)
            self.mgr.inbox.put(m)

    def filter_network_msg(self, message):
        try:
            m = unpack(message)
        except Exception as e:
            print "Garbage Message recevied: ", message
            print "Exception: ", e.message
            return None

        if type(m) == type(ProxyActorMessage()):
            # handled in handle_ProxyActorMessage function
            gevent.spawn(self.handle_ProxyActorMessage, m)
            return None
        else:
            return m


    def cleanup(self):
        print "cleanup..."

        for s in self.__subscribers__:
            s.close()

        for p in self.__publishers__:
            p.close()

        self.context.term()
        

if __name__ == "__main__":
    ProxyActor(my_ip="192.168.2.115").join()
