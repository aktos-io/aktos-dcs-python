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

    def __init__(self, my_ip="", brokers="", rx_port=5012, tx_port=5013):
        """
        brokers: additional brokers other than localhost.
            format: "ip:rx_port:tx_port other_ip:its_rx_port:its_tx_port"
            example: brokers="192.168.2.55:8012:8013 localhost:9012:9013 82.64.123.233:4567:8907"
        """
        #super(ProxyActor, self).__init__()
        Actor.__init__(self)
        print "proxy actor created with id: ", self.actor_id

        self.brokers = brokers
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

        self.__subscribers__ = [self.server_sub,
                           self.client_sub,
                           self.broker_sub]

        self.__publishers__ = [self.server_pub,
                           self.client_pub,
                           self.broker_pub]

        for s in self.__subscribers__:
            s.setsockopt(zmq.SUBSCRIBE, '')

        for p in self.__publishers__:
            p.setsockopt(zmq.LINGER, 0)
            p.setsockopt(zmq.SNDHWM, 2)
            p.setsockopt(zmq.SNDTIMEO, 0)


        # spawn the receivers
        __receivers__ = [self.server_sub_receiver,
                         self.client_sub_receiver,
                         self.broker_sub_receiver]
        for r in __receivers__:
            gevent.spawn(r)

        # server_pub will serve on a random port
        self.server_pub_port = self.server_pub.bind_to_random_port(addr="tcp://*")
        self.server_sub_port = self.server_sub.bind_to_random_port(addr="tcp://*")
        print "this actor's server ports are: ", self.server_sub_port, self.server_pub_port

        self.this_contact = dict()
        self.this_contact[self.my_ip] = [[self.server_sub_port, self.server_pub_port]]
        self.introduction_msg = ProxyActorMessage(new_entry=self.this_contact)
        self.contact_list = dict(self.this_contact)

        # create or try to create address broker
        self.this_is_the_broker = False
        try:
            self.create_broker(watch=False)
        except:
            gevent.spawn(self.create_broker, watch=True)

        self.sync_contacts()

    def sync_contacts(self):
        # go and get other processes' address information
        # connect their server_pub port with your client_sub port

        do_sync = False
        if not self.this_is_the_broker:
            do_sync = True
            self.client_pub.connect("tcp://%s:%d" % ("localhost", self.rx_port))
            self.client_sub.connect("tcp://%s:%d" % ("localhost", self.tx_port))

        broker_list = self.brokers.split()
        if broker_list:
            do_sync = True
            for broker in broker_list:
                ip, rx_port, tx_port = broker.split(":")
                print "  * additional broker: ", ip, rx_port, tx_port
                self.client_pub.connect("tcp://%s:%s" % (ip, rx_port))
                self.client_sub.connect("tcp://%s:%s" % (ip, tx_port))

        if do_sync:
            print "sync contacts..."
            gevent.sleep(2)  # TODO: remove this sleep
            self.propogate_msg_to_others(self.introduction_msg)
        else:
            print "there are no processes to sync contacts..."

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
                gevent.sleep(1)  # TODO: make this time configurable

            gevent.sleep()

    def propogate_msg_to_others(self, msg):
        self.server_send(msg)
        self.broker_send(msg)
        self.client_send(msg)

    def receive(self, msg):
        #print "receive propogating message to others...", msg
        self.propogate_msg_to_others(msg)

    def handle_ProxyActorMessage(self, msg):
        print "debug: ProxyActorMessage received"
        if msg.new_entry:
            print "found new entry, adding current contact list..."
            for k, v in msg.new_entry.iteritems():
                for process in v:
                    try:
                        assert(self.contact_list[k])
                    except:
                        self.contact_list[k] = list()

                    self.contact_list[k].append(process)

            #pdb.set_trace()
            self.propogate_msg_to_others(ProxyActorMessage(
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
                        connect_to = dict()  # ip, rx_port, tx_port
                        if k == self.my_ip:
                            if ports not in my_ports:
                                # other than this process
                                print "will connect to: ", ports
                                connect_to['ip'] = "localhost"
                                connect_to['rx'] = ports[0]
                                connect_to['tx'] = ports[1]
                        else:
                            print "will connect to", k, ports, self.my_ip
                            connect_to['ip'] = k
                            connect_to['rx'] = ports[0]
                            connect_to['tx'] = ports[1]

                        if connect_to:
                            self.client_pub.connect("tcp://%s:%d" % (connect_to['ip'], connect_to['rx']))
                            self.client_sub.connect("tcp://%s:%d" % (connect_to['ip'], connect_to['tx']))


            # simply update the contact list
            self.contact_list = msg.contact_list

            print "replaced contact list: "
            pprint(self.contact_list)

    def server_sub_receiver(self):
        while True:
            message = self.server_sub.recv()
            self.send_to_inner_actors(message)
            self.forward_messages_via_broker(message)
            gevent.sleep()

    def client_sub_receiver(self):
        while True:
            message = self.client_sub.recv()
            self.send_to_inner_actors(message)
            self.forward_messages_via_broker(message)
            gevent.sleep()

    def broker_sub_receiver(self):
        while True:
            message = self.broker_sub.recv()
            self.send_to_inner_actors(message)

            # forward this message to others
            msg = unpack(message)
            if type(msg) != type(ProxyActorMessage()):
                self.server_send(msg)
                self.client_send(msg)

            gevent.sleep()

    def server_send(self, msg):
        msg = unpack(pack(msg))
        msg.sender.append(self.actor_id)
        message = pack(msg)
        self.server_pub.send(message)

    def client_send(self, msg):
        msg = unpack(pack(msg))
        msg.sender.append(self.actor_id)
        message = pack(msg)
        self.client_pub.send(message)

    def broker_send(self, msg):
        if self.this_is_the_broker:
            msg = unpack(pack(msg))
            msg.sender.append(self.actor_id)
            message = pack(msg)
            self.broker_pub.send(message)

    def send_to_inner_actors(self, message):
        msg = unpack(message)
        if type(msg) == type(ProxyActorMessage()):
            # handled in handle_ProxyActorMessage function
            self.handle_ProxyActorMessage(msg)
        else:
            # do not modify msg.sender information
            msg.sender.append(self.actor_id)
            msg = unpack(pack(msg))
            self.mgr.inbox.put(msg)

    def forward_messages_via_broker(self, message):
        msg = unpack(message)
        self.broker_send(msg)

    def cleanup(self):
        print "cleanup..."

        for s in self.__subscribers__:
            s.close()

        for p in self.__publishers__:
            p.close()

        self.context.term()
        

if __name__ == "__main__":
    ProxyActor(my_ip="192.168.2.115").join()
