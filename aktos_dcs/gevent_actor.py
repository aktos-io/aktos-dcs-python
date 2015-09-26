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

class ActorBase(gevent.Greenlet):
    DEBUG_NETWORK_MESSAGES = False
    DEBUG_INNER_MESSAGES = False

    def __init__(self, start_on_init=True):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)
        gevent.signal(signal.SIGTERM, self.__cleanup)
        gevent.signal(signal.SIGINT, self.__cleanup)

        self.actor_id = shortuuid.ShortUUID().random(length=5)

        def dummy_broadcast(msg):
            print "broadcasting msg (DUMMY) : ", msg
        self.broadcast_inbox = dummy_broadcast

        self.msg_serial = 0
        if start_on_init:
            self.start()
        self.msg_history = []

        self.sem = Semaphore()
        #atexit.register(self.__cleanup)

        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        self.handle_functions = {}
        for f in functions:
            if f[0].startswith("handle_"):
                #print "this is handle funct: ", f
                self.handle_functions[f[0]] = f[1]

    def __cleanup(self, *args, **kwargs):
        #print "cleaning up!"
        self.running = False
        self.cleanup()

        # TODO: kill properly!
        self.kill()
        #print "args", args, kwargs
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
        try:
            assert msg['reply_for'] == self.waiting_msg
            self.block = False
        except:
            pass

        for subject in msg['payload']:
            #self.handle_functions.get("handle_" + subject, self.receive)(msg)

            handler = self.handle_functions.get("handle_" + subject, self.receive)
            #handler(msg)
            try:
                assert msg['asked'] in ['anyone', self.actor_id, self.actor_name]
                gevent.spawn(self.blocker_handler, handler, msg)
            except:
                gevent.spawn(handler, msg)

    def blocker_handler(self, orig_handler, msg):
        orig_handler(msg)

        reply_payload = {'CtrlMessage': {}}
        reply_msg = envelp(reply_payload, self.get_msg_id())
        reply_msg['reply_for'] = msg['msg_id']
        self.send_raw(reply_msg)

    def _run(self):
        self.running = True

        def get_message():
            while self.running:
                msg = self.inbox.get()
                self.dispatch_msg(msg)
                gevent.sleep(0)

        gevent.spawn(self.action)
        gevent.spawn(get_message)
        while True:
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
        # without this dela, following code is not working:
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

    def ask(self, msg, to='anyone'):
        msg_id = self.get_msg_id()
        msg = envelp(msg, msg_id)
        msg['asked'] = to
        self.send_raw(msg)
        self.block = True
        self.waiting_msg = msg_id
        while self.block:
            gevent.sleep(0.000001)

class Actor(ActorBase):
    def __init__(self, name=None):
        ActorBase.__init__(self)
        self.mgr = ActorManager()
        self.mgr.register(self)
        self.broadcast_inbox = self.mgr.inbox.put
        self.actor_name = name if name else self.actor_id

class Singleton(type):
    """
    Usage example:

        class my_singleton_class(some_other_class):
            __metaclass__ = Singleton

            ... class definition as usual

    """
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__instance = None
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance


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
