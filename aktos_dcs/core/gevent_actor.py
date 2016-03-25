#!/usr/bin/env python
# coding: utf-8

import gevent
from gevent.queue import Queue
import atexit
from wait_all import wait_all
import inspect
import shortuuid
from messages import *
from gevent.lock import Semaphore
import signal
from gevent.hub import GreenletExit
import re
from cca_signal import CcaSignalLoop
from singleton import Singleton

class ActorBase(object):
    DEBUG_NETWORK_MESSAGES = False
    DEBUG_INNER_MESSAGES = False

    def __init__(self, start_on_init=True):

        self.inbox = Queue()
        gevent.signal(signal.SIGTERM, self.__cleanup)
        gevent.signal(signal.SIGINT, self.__cleanup)

        self.actor_id = shortuuid.ShortUUID().random(length=5)

        def dummy_broadcast(msg):
            print "broadcasting msg (DUMMY) : ", msg
        self.broadcast_inbox = dummy_broadcast

        self.msg_serial = 0
        self.msg_history = []

        self.sem = Semaphore()
        #atexit.register(self.__cleanup)

        if start_on_init:
            self.start()

        # action functions, such as "action, action1, action2, ..., action999"
        self.action_funcs = []
        action_funcs_pattern = re.compile("^action_?[0-9]*$")

        # handle functions, such as "handle_MyMessage"
        self.handle_functions = {}

        # plc_loop functions, such as "plc_loop, plc_loop1, ..., plc_loop999"
        self.plc_funcs = []
        plc_funcs_pattern = re.compile("^plc_loop_?[0-9]*$")


        # spawn automatic functions
        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        for f in functions:
            if f[0].startswith("handle_"):
                #print "this is handle funct: ", f
                self.handle_functions[f[0]] = f[1]

            if action_funcs_pattern.match(f[0]):
                self.action_funcs.append(f[1])

            if plc_funcs_pattern.match(f[0]):
                self.plc_funcs.append(f[1])


    def prepare(self):
        """
        Prepare objects before using them

        Define in your class
        """
        pass

    def start(self):
        self.prepare()
        self.main_greenlet = gevent.spawn(self._run)

    def kill(self, *args, **kwargs):
        self.__cleanup()

    def __cleanup(self, *args, **kwargs):
        #print "cleaning up!"
        self.running = False
        self.cleanup()

        try:
            for i in self.plc_loop_greenlets:
                i.kill()

            for i in self.action_greenlets:
                i.kill()

            self.get_message_greenlet.kill()
            self.main_greenlet.kill()
        except:
            print "Killed actor..."

        raise GreenletExit


    def get_msg_id(self):
        msg_id = '.'.join([self.actor_id, str(self.msg_serial)])
        self.msg_serial += 1
        return msg_id

    def receive(self, msg):
        """
        Define in your subclass.
        """
        pass

    def action(self):
        """
        Define in your subclass.
        """
        pass

    def cleanup(self):
        """
        Define in your subclass.
        """
        pass

    def dispatch_msg(self, msg):
        for subject in msg['payload']:
            #self.handle_functions.get("handle_" + subject, self.receive)(msg)

            handler = self.handle_functions.get("handle_" + subject, self.receive)
            #handler(msg)
            if handler != self.receive:
                msg_single = msg["payload"][subject]
            else:
                msg_single = msg
            gevent.spawn(handler, msg_single)

    def template_plc_loop(self, plc_loop_func):
        while True:
            plc_loop_func()
            CcaSignalLoop().loop_point()
            gevent.sleep(0.01)

    def _run(self):
        self.running = True

        # fire actions
        self.action_greenlets = []
        for i in self.action_funcs:
            self.action_greenlets.append(gevent.spawn(i))

        # fire plc_loops
        self.plc_loop_greenlets = []
        for i in self.plc_funcs:
            self.plc_loop_greenlets.append(gevent.spawn(self.template_plc_loop, i))

        # fire message receiver
        def get_message():
            while self.running:
                msg = self.inbox.get()
                self.dispatch_msg(msg)
                gevent.sleep(0)
        self.get_message_greenlet = gevent.spawn(get_message)
        while self.running:
            gevent.sleep(99999)

    def send(self, msg):
        """
        send message to the actor manager
        """
        #assert(isinstance(msg, Message))

        msg = envelp(msg, self.get_msg_id())
        self.send_raw(msg)

        # TODO: Fix this: this little delay is to be able to
        # send messages one after the other
        #
        # without this delay, following code is not working:
        #
        #      the_actor.send({'a': 'message'})
        #      the_actor.send({'a': 'different message'})
        #
        gevent.sleep(0.000000000000000000000000001)

    def send_raw(self, msg):
        msg['sender'].append(self.actor_id)
        if self.DEBUG_INNER_MESSAGES:
            print "sending msg to manager: ", msg
        self.broadcast_inbox(msg)

        # give control to another greenlet
        #gevent.sleep()


class Actor(ActorBase):
    def __init__(self, name=None):
        ActorBase.__init__(self, start_on_init=False)
        self.mgr = ActorManager()
        self.mgr.register(self)
        self.broadcast_inbox = self.mgr.inbox.put
        self.actor_name = name if name else self.actor_id
        self.start()

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            if name.startswith("send_"):
                msg_topic = name.split("_")[1]
                #print "Msg name: ", msg_topic

                def msg_sender(self, *args, **kwargs):
                    m = {msg_topic: kwargs}
                    self.send(m)

                import types
                setattr(self, name, types.MethodType(msg_sender, self))
                return object.__getattribute__(self, name)
            else:
                raise



class ActorManager(ActorBase):
    __metaclass__ = Singleton

    def __init__(self):
        ActorBase.__init__(self)

        # actor_obj: "actor name" [default: None]
        self.actors = []
        self.actor_inboxes = []

    def receive(self, msg):
        #start_time = time.time()
        for inbox in [i[1] for i in self.actor_inboxes if i[0] not in msg['sender']]:
            inbox(msg)
        #print "manager dispatched messages in %f secs" % (time.time() - start_time)

    def register(self, actor_instance):
        self.actors.append(actor_instance)
        self.actor_inboxes.append([actor_instance.actor_id, actor_instance.inbox.put])

    def dispatch_msg(self, msg):
        gevent.spawn(self.receive, msg)

if __name__ == "__main__":
    # TODO: add tests here
    class TestActor(Actor):
        def handle_IoMessage(self, msg):
            msg = get_msg_body(msg)
            if msg['pin-name'] == 'hello':
                print "got message from pin named 'hello':", msg

    class TestActor2(Actor):
        def action(self):
            val = 0
            while True:
                val += 1
                self.send({'IoMessage':
                               {'pin-name': 'hello',
                                'val': val
                                }})
                gevent.sleep(0.01)

    TestActor()
    TestActor2()
    # cpu: 40%
    wait_all()
