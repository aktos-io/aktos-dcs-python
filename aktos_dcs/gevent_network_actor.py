# coding: utf-8
__author__ = 'ceremcem'

import gevent
from cca_messages import *
from gevent_actor import Actor, Singleton
import zmq.green as zmq

from gevent import socket

from pprint import pprint

if zmq.zmq_version_info()[0] < 4:
    raise Exception("libzmq version should be >= 4.x")

import pdb

def get_local_ip_addresses():
    import netifaces

    ip_addresses = list()
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i == 'lo':
            continue
        iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if iface != None:
            for j in iface:
                addr = j['addr']
                if addr != '127.0.0.1':
                    ip_addresses.append(addr)
    return ip_addresses

class DcsContactList():
    #__metaclass__ = Singleton

    def __init__(self, contact_str="", ip=[], rx=0, tx=0):
        self.contact_list = list()

        if contact_str:
            self.add_from_contact_str(contact_str)
        elif ip:
            self.add_contact(ip_addresses=ip, rx_port=rx, tx_port=tx)

    def add_contact(self, ip_addresses=[], rx_port=0, tx_port=0):
        """
        contact format:

            {'ip-list': [ip, ...],
            'ports': [rx, tx],
            }
        """
        if type(ip_addresses) != type(list()):
            ip_addresses = [ip_addresses]

        contact = dict()
        contact['ip-list'] = ip_addresses
        contact["ports"] = [int(rx_port), int(tx_port)]
        self.contact_list.append(contact)

    def add_from_contact_list(self, contact_list):
        """
        contact list format:

            [contact, contact, ...]

        """
        for c in contact_list:
            if c not in self.contact_list:
                print "adding contact to the contact list: ", c
                self.contact_list.append(c)

    def add_from_contact_str(self, contact_str):
        """
        contact_str format: "ip:rx_port:tx_port other_ip:its_rx_port:its_tx_port"

            example: "192.168.2.55:8012:8013 localhost:9012:9013 82.64.123.233:4567:8907"
        """
        result = dict()
        broker_list = contact_str.split()
        if broker_list:
            for broker in broker_list:
                ip, rx_port, tx_port = broker.split(":")
                self.add_contact(ip_addresses=[ip], rx_port=rx_port, tx_port=tx_port)


class Link(dict):
    """
    # server_link:
    #   inner messages forwarded to server_pub
    #   server_sub forwards to actor manager
    #
    # client_link:
    #   inner messages forwarded to client_pub
    #   client_sub forwards to actor manager
    #
    # broker_link:
    #   this is address broker. others connect to
    #   this link and exchange known publisher's
    #   address+port information (phone book)
    #
    # broker_client_link:
    #   connect to the broker using this link
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

        self.server = LinkMethods()
        self.client = LinkMethods()
        self.broker = LinkMethods()
        self.broker_client = LinkMethods()

class LinkMethods(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        self.sub = None
        self.pub = None
        self.receiver = None


class ProxyActor(Actor):

    def __init__(self, brokers="", proxy_brokers="", rx_port=5012, tx_port=5013):
        """
        brokers / proxy brokers: additional brokers / proxies to connect to

            example: brokers="192.168.2.55:8012:8013 localhost:9012:9013 82.64.123.233:4567:8907"

        """
        Actor.__init__(self)
        print "proxy actor created with id: ", self.actor_id

        self.brokers = brokers
        self.proxy_brokers = proxy_brokers
        self.my_ip = get_local_ip_addresses()
        self.rx_port = rx_port
        self.tx_port = tx_port
        self.contacts = DcsContactList()
        self.context = zmq.Context()
        self.msg_history = []  # list of [msg_id, timestamp]
        self.connection_list = []

        self.link = Link()

        # spawn the receivers
        self.link.broker.receiver = self.broker_sub_receiver
        self.link.server.receiver = self.server_sub_receiver
        self.link.client.receiver = self.client_sub_receiver
        self.link.broker_client.receiver = self.broker_client_sub_receiver

        for l in self.link:
            self.link[l].sub = self.context.socket(zmq.SUB)
            self.link[l].sub.setsockopt(zmq.SUBSCRIBE, '')

            self.link[l].pub = self.context.socket(zmq.PUB)
            self.link[l].pub.setsockopt(zmq.LINGER, 0)
            self.link[l].pub.setsockopt(zmq.SNDHWM, 2)
            self.link[l].pub.setsockopt(zmq.SNDTIMEO, 0)

            gevent.spawn(self.link[l].receiver)

        # create or watch to create address broker
        self.this_is_the_broker = False
        try:
            self.create_broker(watch=False)
        except:
            gevent.spawn(self.create_broker, watch=True)
            # server_pub will serve on a random port

        self.server_pub_port = self.link.server.pub.bind_to_random_port(addr="tcp://*")
        self.server_sub_port = self.link.server.pub.bind_to_random_port(addr="tcp://*")
        print "this actor's server ports are: ", self.server_sub_port, self.server_pub_port

        self.this_contact = DcsContactList(ip=self.my_ip, rx=self.server_sub_port, tx=self.server_pub_port)
        self.contacts.add_from_contact_list(self.this_contact.contact_list)

        # add proxy brokers to contact list
        self.contacts.add_from_contact_str(self.proxy_brokers)

        self.sync_contacts()

    def connect_to_contacts(self, link_methods=LinkMethods(), contact_list=[]):
        rx, tx = sub, pub = 0, 1
        #print "will connect to contact list: ", contact_list
        for contact in contact_list:
            if contact not in self.this_contact.contact_list:
                for ip in contact['ip-list']:
                    conn_str = "%s:%d:%d" % (ip, contact['ports'][rx], contact['ports'][tx])
                    print "connecting to ", conn_str
                    rx_addr = "tcp://%s:%d" % (ip, contact['ports'][rx])
                    tx_addr = "tcp://%s:%d" % (ip, contact['ports'][tx])
                    link_methods.pub.connect(rx_addr)
                    link_methods.sub.connect(tx_addr)
                    self.connection_list.append(conn_str)
                    #print "full connection list: ", self.connection_list
            else:
                #print "not connecting to itself: ", contact
                pass


    def sync_contacts(self):
        # go and get other processes' address information
        # connect their server_pub port with your client_sub port

        print "sync contacts..."  #, self.contacts.contact_list

        if not self.this_is_the_broker:
            local_broker_contact = DcsContactList("localhost:%d:%d" % (self.rx_port, self.tx_port))
            self.connect_to_contacts(self.link.broker_client, local_broker_contact.contact_list)

        self.connect_to_contacts(self.link.broker_client, self.contacts.contact_list)

        gevent.sleep(2)  # TODO: remove this sleep

        self.introduction_msg = ProxyActorMessage(new_entry=self.contacts.contact_list)
        self.broker_client_send(self.introduction_msg)

    def create_broker(self, watch=False):
        while True:
            try:
                rx_addr = "tcp://%s:%d" % ("*", self.rx_port)
                tx_addr = "tcp://%s:%d" % ("*", self.tx_port)

                self.link.broker.sub.bind(rx_addr)
                self.link.broker.pub.bind(tx_addr)
                print "this actor created a broker"

                self.this_is_the_broker = True

                if watch:
                    # TODO: if broker created while watching,
                    # then there is a random server port created already.
                    # others are connected to that port already. handle this
                    # situation.

                    print "TODO: TEST THIS! broker_client disconnecting from itself..."
                    self.link.broker_client.pub.disconnect("tcp://%s:%d" % ("localhost", self.rx_port))
                    self.link.broker_client.sub.disconnect("tcp://%s:%d" % ("localhost", self.tx_port))

                break  # quit trying to create a broker
            except Exception as e:
                if not watch:
                    raise
                gevent.sleep(1)  # TODO: make this time configurable

            gevent.sleep()

    def receive(self, msg):
        #print "receive propogating message to others...", msg
        self.server_send(msg)
        self.client_send(msg)

    def handle_ProxyActorMessage(self, msg):
        print ".......... ProxyActorMessage received"
        if msg.new_entry:
            print "found new entry, adding current contact list..."
            self.contacts.add_from_contact_list(msg.new_entry)
            #pdb.set_trace()
            self.broker_send(ProxyActorMessage(
                contact_list=self.contacts.contact_list,
                reply_to=msg.msg_id))

        if msg.contact_list:
            print "merged with full contact list... "
            self.contacts.add_from_contact_list(msg.contact_list)
            self.connect_to_contacts(link_methods=self.link.client, contact_list=msg.contact_list)

        #pprint(self.contacts.contact_list)

    def server_sub_receiver(self):
        while True:
            message = self.link.server.sub.recv()
            print "server sub received: ", message
            msg = self.filter_unpack(message)
            if msg:
                self.send_to_inner_actors(msg)
            gevent.sleep()

    def client_sub_receiver(self):
        while True:
            message = self.link.client.sub.recv()
            #print "client sub received: ", message
            msg = self.filter_unpack(message)
            if msg:
                self.send_to_inner_actors(msg)
            gevent.sleep()

    def broker_sub_receiver(self):
        while True:
            message = self.link.broker.sub.recv()
            print "broker sub received: ", message
            msg = self.filter_unpack(message)
            if msg:
                self.send_to_inner_actors(msg)
            gevent.sleep()

    def add_sender_to_msg(self, msg):
        try:
            assert msg.sender[-1] == self.actor_id
        except:
            msg.sender.append(self.actor_id)

    def broker_client_sub_receiver(self):
        while True:
            message = self.link.broker_client.sub.recv()
            print "broker_client sub received: ", message

            # process the control message
            msg = self.filter_unpack(message)
            if msg:
                if type(msg) == type(ProxyActorMessage()):
                    gevent.spawn(self.handle_ProxyActorMessage, msg)
            gevent.sleep()

    def filter_unpack(self, message):
        msg_timeout = 1
        msg = unpack(message)
        if self.actor_id in msg.sender:
            print "dropping short circuit message..."
            pass
        elif msg.msg_id in [i[0] for i in self.msg_history]:
            print "dropping duplicate message..."
        elif msg.timestamp + msg_timeout < time.time():
            print "dropping timeouted message (%d secs. old)" % (time.time() - msg.timestamp)
        else:
            self.msg_history.append([msg.msg_id, msg.timestamp])
            # TODO: find more efficient way to do this
            if self.msg_history:
                if self.msg_history[0][1] + msg_timeout< time.time():
                    del self.msg_history[0]
            return msg
        return None

    def server_send(self, msg):
        self.add_sender_to_msg(msg)
        msg.debug.append("server-send")
        message = pack(msg)
        self.link.server.pub.send(message)

    def client_send(self, msg):
        self.add_sender_to_msg(msg)
        msg.debug.append("client-send")
        message = pack(msg)
        self.link.client.pub.send(message)

    def broker_send(self, msg):
        self.add_sender_to_msg(msg)
        msg.debug.append("broker/broker-client-send")
        message = pack(msg)

        if self.this_is_the_broker:
            self.link.broker.pub.send(message)
        self.link.broker_client.pub.send(message)

    def broker_client_send(self, msg):
        self.broker_send(msg)

    def send_to_inner_actors(self, msg):
        if type(msg) == type(ProxyActorMessage()):
            # handled in handle_ProxyActorMessage function
            gevent.spawn(self.handle_ProxyActorMessage, msg)
        else:
            self.add_sender_to_msg(msg)
            self.mgr.inbox.put(msg)

    def forward_messages_via_broker(self, msg):
        self.broker_send(msg)

    def cleanup(self):
        print "cleanup..."

        for l in self.link:
            self.link[l].sub.close()
            self.link[l].pub.close()

        self.context.term()
        

if __name__ == "__main__":
    ProxyActor().join()
