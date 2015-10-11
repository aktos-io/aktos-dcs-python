# coding: utf-8
__author__ = 'ceremcem'

import gevent
from gevent_actor import Actor
import zmq.green as zmq
from messages import *
from gevent import socket
from pprint import pprint
import copy

if zmq.zmq_version_info()[0] < 4:
    raise Exception("libzmq version should be >= 4.x")

def get_local_ip_addresses():
    import netifaces

    ip_addresses = list()
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i == 'lo':
            continue
        iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if iface:
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
                msg = "adding to the contact list: " + display_contact(c)
                print color.color(msg, fg_blue=True)
                self.contact_list.append(c)

    def add_from_contact_str(self, contact_str):
        """
        contact_str format: "ip:rx_port:tx_port other_ip:its_rx_port:its_tx_port"

            example: "192.168.2.55:8012:8013 localhost:9012:9013 82.64.123.233:4567:8907"
        """
        broker_list = contact_str.split()
        if broker_list:
            for broker in broker_list:
                ip, rx_port, tx_port = broker.split(":")
                self.add_contact(ip_addresses=[ip], rx_port=rx_port, tx_port=tx_port)

import color
def display_contact(contact):
    ip_list = '/'.join(contact['ip-list'])
    r = '\t%s\t%d %d' % (ip_list, contact['ports'][0], contact['ports'][1])
    return r


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
        self.link.broker.receiver = self.broker_sub_receiver
        self.link.server.receiver = self.server_sub_receiver
        self.link.client.receiver = self.client_sub_receiver
        self.link.broker_client.receiver = self.broker_client_sub_receiver

        # create sub, pub and spawn the receivers
        for l in dict(self.link).values():
            l.sub = self.context.socket(zmq.SUB)
            l.sub.setsockopt(zmq.SUBSCRIBE, '')
            l.sub.setsockopt(zmq.LINGER, 0)
            l.sub.setsockopt(zmq.RCVHWM, 0)

            l.pub = self.context.socket(zmq.PUB)
            l.pub.setsockopt(zmq.LINGER, 0)
            l.pub.setsockopt(zmq.SNDHWM, 0)

            gevent.spawn(l.receiver)

        self.create_server_on_a_random_port()

        # add proxy brokers to contact list
        self.contacts.add_from_contact_str(self.proxy_brokers)
        self.connect_to_contacts('client', self.contacts.contact_list)

        # create or watch to create address broker
        self.this_is_the_broker = False
        try:
            self.create_broker(watch=False)
        except:
            gevent.spawn(self.create_broker, watch=True)
            self.sync_contacts()



        gevent.sleep(2) #TODO: change this with "as soon as connected all of the others"


    def create_server_on_a_random_port(self):
        self.server_pub_port = self.link.server.pub.bind_to_random_port(addr="tcp://*")
        self.server_sub_port = self.link.server.sub.bind_to_random_port(addr="tcp://*")
        print "this actor's server ports are: ", self.server_sub_port, self.server_pub_port

        self.this_contact = DcsContactList(ip=self.my_ip, rx=self.server_sub_port, tx=self.server_pub_port)
        self.contacts.add_from_contact_list(self.this_contact.contact_list)

    def connect_to_contacts(self, link_name, contact_list=[]):
        rx, tx = sub, pub = 0, 1
        #print "will connect to contact list: ", contact_list
        for contact in contact_list:
            if contact not in self.this_contact.contact_list:
                for ip in contact['ip-list']:
                    conn_str = "%s:%d:%d" % (ip, contact['ports'][rx], contact['ports'][tx])
                    print_msg = ("%s\t%d %d\tvia %s" %
                          (ip, contact['ports'][rx], contact['ports'][tx], link_name))
                    print_msg = color.color(print_msg, fg_light_green=True)
                    print color.color("connecting to\t", fg_green=True) + print_msg
                    rx_addr = "tcp://%s:%d" % (ip, contact['ports'][rx])
                    tx_addr = "tcp://%s:%d" % (ip, contact['ports'][tx])
                    self.link[link_name].pub.connect(rx_addr)
                    self.link[link_name].sub.connect(tx_addr)
                    self.connection_list.append(conn_str)

                    #print "full connection list: ", self.connection_list
            else:
                m = "not connecting to itself: " + display_contact(contact)
                print color.color(m, fg_orange=True)
                pass

    def sync_contacts(self):
        # go and get other processes' address information
        # connect their server_pub port with your client_sub port

        print "sync contacts..."  #, self.contacts.contact_list

        if not self.this_is_the_broker:
            print "this is not the broker..."
            local_broker_contact = DcsContactList("localhost:%d:%d" % (self.rx_port, self.tx_port))
            self.connect_to_contacts('broker_client', local_broker_contact.contact_list)
        other_brokers = DcsContactList(self.brokers)
        self.connect_to_contacts('broker_client', other_brokers.contact_list)

        gevent.sleep(2)  # TODO: remove this sleep

        self.introduction_msg = envelp(
            {'ProxyActorMessage': {'new_contact_list': self.contacts.contact_list}},
            self.get_msg_id())
        self.broker_client_send(self.introduction_msg)
        self.broker_send(self.introduction_msg)

    def handle_ProxyActorMessage(self, msg_raw):
        msg = get_msg_body(msg_raw)
        print "CM delay: ", (time.time() - msg_raw['timestamp'])
        if 'new_contact_list' in msg:
            print "got new contact list, merging and redistributing..."
            #pprint(msg)
            self.contacts.add_from_contact_list(msg['new_contact_list'])
            #pdb.set_trace()
            self.broker_all_send(envelp({'ProxyActorMessage':
                {'contact_list': self.contacts.contact_list,
                'reply_to': msg_raw['msg_id']}}, self.get_msg_id()))
        elif 'contact_list' in msg:
            print "got full contact list, updating own list... "
            self.contacts.add_from_contact_list(msg['contact_list'])
            if msg['reply_to'] == self.introduction_msg['msg_id']:
                print "connecting whole contact list..."
                self.connect_to_contacts('client', contact_list=msg['contact_list'])
        else:
            print "WARNING: UNHANDLED CONTROL MESSAGE: ", msg

        #pprint(self.contacts.contact_list)

    def create_broker(self, watch=False):
        while True:
            try:
                rx_addr = "tcp://%s:%d" % ("*", self.rx_port)
                tx_addr = "tcp://%s:%d" % ("*", self.tx_port)

                self.link.broker.sub.bind(rx_addr)
                self.link.broker.pub.bind(tx_addr)
                print "this actor created a broker"

                self.this_is_the_broker = True
                self.sync_contacts()

                if watch:
                    # TODO: if broker created while watching,
                    # then there is a random server port created already.
                    # others are connected to that port already. handle this
                    # situation.

                    # NOTE: this block is tested and working
                    print "broker_client disconnecting from itself..."
                    self.link.broker_client.pub.disconnect("tcp://%s:%d" % ("localhost", self.rx_port))
                    self.link.broker_client.sub.disconnect("tcp://%s:%d" % ("localhost", self.tx_port))


                break  # quit trying to create a broker
            except Exception as e:
                if not watch:
                    raise
                gevent.sleep(1)  # TODO: make this time configurable

            gevent.sleep()

    def receive(self, msg):
        if self.DEBUG_NETWORK_MESSAGES:
            print "forwarding msg to network: ", msg['msg_id']
        self.server_send(msg)
        self.client_send(msg)
        self.broker_send(msg)
        #self.broker_client_send(msg)

    def server_sub_receiver(self):
        #print "server sub receiver started"
        while True:
            message = self.link.server.sub.recv()
            self.broker_all_receive(message, 'server sub')
            gevent.sleep()

    def client_sub_receiver(self):
        #print "client sub receiver started"
        while True:
            message = self.link.client.sub.recv()
            self.broker_all_receive(message, 'client sub')
            gevent.sleep()

    def broker_sub_receiver(self):
        #print "broker sub receiver started"
        while True:
            message = self.link.broker.sub.recv()
            self.broker_all_receive(message, 'broker sub')
            gevent.sleep()

    def broker_client_sub_receiver(self):
        #print "broker client sub receiver started"
        while True:
            message = self.link.broker_client.sub.recv()
            self.broker_all_receive(message, 'broker client sub')
            gevent.sleep()

    def broker_all_receive(self, message, caller=''):
        if caller:
            if self.DEBUG_NETWORK_MESSAGES:
                print caller, " received msg..."
            pass

        #print "proxy actor got message: ", message

        try:
            msg_r = unpack(message)

            msg_r = self.filter_msg(msg_r)
            if msg_r:
                if self.DEBUG_NETWORK_MESSAGES:
                    print "got filtered message: ", msg_r['msg_id']
                self.send_to_inner_actors(msg_r)

                if self.DEBUG_NETWORK_MESSAGES:
                    print "forwarding proxy message ", msg_r['payload'].keys()[0], msg_r['msg_id']
                self.broker_send(msg_r)
                self.client_send(msg_r)
                self.server_send(msg_r)
        except:
            pass

    def server_send(self, msg_raw):
        self.add_sender_to_msg(msg_raw)
        #msg2 = unpack(pack(msg))
        #msg2.debug.append("server-send")
        #print "server_send..."
        message = pack(msg_raw)
        self.link.server.pub.send(message)

    def client_send(self, msg_raw):
        self.add_sender_to_msg(msg_raw)
        #msg2 = unpack(pack(msg))
        #msg2.debug.append("client-send")
        #print "client_send..."
        message = pack(msg_raw)
        self.link.client.pub.send(message)

    def broker_send(self, msg_raw):
        if self.this_is_the_broker:
            #pdb.set_trace()
            self.add_sender_to_msg(msg_raw)
            #msg2 = unpack(pack(msg))
            #msg2.debug.append("broker-send")
            #print "broker_send..."
            message = pack(msg_raw)
            self.link.broker.pub.send(message)

    def broker_client_send(self, msg_raw):
        self.add_sender_to_msg(msg_raw)
        #msg2 = unpack(pack(msg))
        #msg2.debug.append("broker-client-send")
        message = pack(msg_raw)
        #print "broker_client_send..."
        self.link.broker_client.pub.send(message)

    def broker_all_send(self, msg_raw):
        self.broker_send(msg_raw)
        self.broker_client_send(msg_raw)

    def add_sender_to_msg(self, msg_raw):
        if self.actor_id not in msg_raw['sender']:
            msg_raw['sender'].append(self.actor_id)

    def send_to_inner_actors(self, msg_raw):
        if self.DEBUG_NETWORK_MESSAGES:
            print "forwarding msg to manager: ", msg_raw['msg_id']
        if 'ProxyActorMessage' in msg_raw['payload']:
            # handled in handle_ProxyActorMessage function
            gevent.spawn(self.handle_ProxyActorMessage, msg_raw)
        else:
            self.add_sender_to_msg(msg_raw)
            self.mgr.inbox.put(msg_raw)

    def filter_msg(self, msg):
        # NOTE: THIS FUNCTION SHOULD BE CALL ONLY ONCE
        # (CAN NOT BE CHAINED IN FUNCTIONS). ELSE,
        # ERRONEOUS DUPLICATE MESSAGE EVENT WILL OCCUR
        try:
            self.sem.acquire()
            if self.DEBUG_NETWORK_MESSAGES:
                print "filter process started...", msg
                gevent.sleep()

            msg_filtered = None
            msg_timeout = 5
            if self.actor_id in msg['sender']:
                if self.DEBUG_NETWORK_MESSAGES:
                    print "dropping short circuit message...", msg['msg_id']
                #pprint(self.msg_history)
                pass
            elif msg['msg_id'] in [i[0] for i in self.msg_history]:
                if self.DEBUG_NETWORK_MESSAGES:
                    print "dropping duplicate message...", msg['msg_id']
                pass
            elif msg['timestamp'] + msg_timeout < time.time():
                print "dropping timeouted message (%d secs. old)" % (time.time() - msg['timestamp'])
            else:
                self.msg_history.append(list([msg['msg_id'], msg['timestamp']]))
                msg_filtered = msg

                # Erase messages that will be filtered via "timeout" filter already
                # TODO: find more efficient way to do this
                if self.msg_history:
                    if self.msg_history[0][1] + msg_timeout < time.time():
                        del self.msg_history[0]

                #self.msg_history = [i for i in self.msg_history if i[1] + msg_timeout > time.time()]

                if self.DEBUG_NETWORK_MESSAGES:
                    print "passed filter: ", msg['msg_id']

            if self.DEBUG_NETWORK_MESSAGES:
                print "filter process done..."

            self.sem.release()
            return msg_filtered
        except Exception as e:
            print "DEBUG: unknown message: ", e.message, msg
            return None


    def cleanup(self):
        print "cleanup..."

        for l in self.link:
            self.link[l].sub.close()
            self.link[l].pub.close()

        self.context.term()

if __name__ == "__main__":
    ProxyActor().join()
