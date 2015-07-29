#!/usr/bin/env python
# coding: utf-8

import gevent
from gevent.queue import Queue

import atexit
import traceback
from pprint import pprint

from Messages import *

import uuid

import pdb

from gevent.lock import Semaphore

class ActorBase(gevent.Greenlet):
    DEBUG_NETWORK_MESSAGES = False
    DEBUG_INNER_MESSAGES = False

    def __init__(self, start_on_init=True):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)
        self.actor_id = str(uuid.uuid4())
        if start_on_init:
            self.start()
        self.msg_history = []

        self.sem = Semaphore()
        atexit.register(self.cleanup)

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

    def _run(self):
        self.running = True

        def get_message():
            while self.running:
                msg = self.inbox.get()
                #msg = self.filter_msg(msg)
                if msg:
                    gevent.spawn(self.receive, msg)
                    #print("message handler spawned!!")

                    # pass the XYZMessage to "handle_XYZMessage()"
                    # function if such a function exists:
                    handler_func_name = "handle_" + msg.__class__.__name__
                    handler_func = getattr(self, handler_func_name, None)
                    if callable(handler_func):
                        gevent.spawn(handler_func, msg)

        a = gevent.spawn(get_message)
        b = gevent.spawn(self.action)
        #gevent.joinall([a, b])
        while True:
            gevent.sleep(1)

    def filter_msg(self, msg):
        # NOTE: THIS FUNCTION SHOULD BE CALL ONLY ONCE
        # (CAN NOT BE CHAINED IN FUNCTIONS). ELSE,
        # ERRONEOUS DUPLICATE MESSAGE EVENT WILL OCCUR
        self.sem.acquire()
        if self.DEBUG_NETWORK_MESSAGES:
            print "filter process started..."
            gevent.sleep()
        msg_filtered = None
        msg_timeout = 5
        if self.actor_id in msg.sender:
            if self.DEBUG_NETWORK_MESSAGES:
                print "dropping short circuit message...", msg.msg_id
            #pprint(self.msg_history)
            pass
        elif msg.msg_id in [i[0] for i in self.msg_history]:
            if self.DEBUG_NETWORK_MESSAGES:
                print "dropping duplicate message...", msg.msg_id
            pass
        elif msg.timestamp + msg_timeout < time.time():
            print "dropping timeouted message (%d secs. old)" % (time.time() - msg.timestamp)
        else:
            self.msg_history.append(list([msg.msg_id, msg.timestamp, msg.debug]))
            msg_filtered = msg

            # Erase messages that will be filtered via "timeout" filter already
            # TODO: find more efficient way to do this
            if self.msg_history:
                if self.msg_history[0][1] + msg_timeout < time.time():
                    del self.msg_history[0]

            if self.DEBUG_NETWORK_MESSAGES:
                print "passed filter: ", msg.msg_id

        if self.DEBUG_NETWORK_MESSAGES:
            print "filter process done..."

        self.sem.release()
        return msg_filtered

class Actor(ActorBase):

    def __init__(self):
        ActorBase.__init__(self)
        self.mgr = ActorManager()
        self.mgr.register(self)

    def send(self, msg):
        """
        send message to the actor manager
        """
        assert(isinstance(msg, Message))

        if self.DEBUG_INNER_MESSAGES:
            print "sending msg to manager: ", msg.cls
        msg.sender.append(self.actor_id)
        msg.debug.append("actor")

        self.mgr.inbox.put(msg)

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

    def receive(self, msg):
        assert(isinstance(msg, Message))

        for actor in self.actors:
            if actor.actor_id not in msg.sender:
                if self.DEBUG_INNER_MESSAGES:
                    print "manager forwarding message to all actors: ", \
                        actor.actor_id
                msg.debug.append('manager')
                actor.inbox.put(msg)
            else:
                if self.DEBUG_INNER_MESSAGES:
                    print "manager drops short circuit message..."


    def register(self, actor_instance):
        self.actors.append(actor_instance)


if __name__ == "__main__":
    class TestActor(Actor):
        def receive(self, message):
            print "TestActor.receive: ", message, id(self)

        def handle_TestMessage(self, msg):
            print "handle_TestMessage: ", msg

        def handle_IoMessage(self, msg):
            print "handle_IoMessage:", msg

        def cleanup(self):
            print "exiting and cleanup ...", self

    class TestActor2(Actor):
        def receive(self, msg):
            print "this is test actor2", msg, id(self)

    class TestMessage(Message):
        pass

    test = TestActor()
    test11 = TestActor()
    test2 = TestActor2()

    test.inbox.put(TestMessage(deneme="bir kii"))
    test.inbox.put(IoMessage(aaa="io message"))
    #test.inbox.put("bu nesne Message class'ından türetilmedi")

    #test.send("naber")

    gevent.sleep(99999)