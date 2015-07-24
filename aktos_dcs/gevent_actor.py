#!/usr/bin/env python
# coding: utf-8

import gevent
from gevent.queue import Queue

import atexit
import traceback

from cca_messages import *
import uuid

import pdb

class ActorBase(gevent.Greenlet):

    def __init__(self, start_on_init=True):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)
        self.actor_id = str(uuid.uuid4())
        if start_on_init:
            self.start()

        atexit.register(self.cleanup)

    def receive(self, msg):
        """
        Define in your subclass.
        """
        #raise NotImplemented()
        pass

    def action(self):
        pass

    def cleanup(self):
        #print "this is an actor, running cleanup...", self
        pass

    def _run(self):
        self.running = True

        def get_message():
            while self.running:
                message = self.inbox.get()

                gevent.spawn(self.receive, message)
                #print("message handler spawned!!")

                # pass the XYZMessage to "handle_XYZMessage()" function
                # if exists:
                handler_func_name = "handle_" + message.__class__.__name__
                handler_func = getattr(self, handler_func_name, None)
                if callable(handler_func):
                    handler_func(message)


        a = gevent.spawn(get_message)
        b = gevent.spawn(self.action)

        gevent.joinall([a, b])


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

        msg.sender.append(self.actor_id)
        if msg.send_to_itself:
            msg.send_to_itself = None
            self.inbox.put(msg)

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
                actor.inbox.put(msg)

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