#!/usr/bin/env python
# coding: utf-8

import gevent
from gevent.queue import Queue

from cca_messages import *
import uuid


class ActorBase(gevent.Greenlet):

    def __init__(self):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)
        self.actor_id = uuid.uuid4()
        self.start()

    def receive(self, msg):
        """
        Define in your subclass.
        """
        #raise NotImplemented()
        pass

    def action(self):
        pass

    def _run(self):
        self.running = True

        def get_message():
            while self.running:
                message = self.inbox.get()

                gevent.spawn(self.receive, message)
                #print("message handler spawned!!")
                try:
                    if isinstance(message, Message):
                        handler_func = "handle_" + message.__class__.__name__
                        getattr(self, handler_func)(message)
                except AttributeError:
                    pass
                except:
                    raise

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
        try:
            msg = unpack(msg)
        except:
            pass
        if isinstance(msg, Message):
            msg.sender = self.actor_id
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
        try:
            msg = unpack(msg)
        except:
            pass
        for actor_obj in self.actors:
            if msg.sender != actor_obj.actor_id:
                actor_obj.inbox.put(msg)

    def register(self, actor_instance):
        self.actors.append(actor_instance)



if __name__ == "__main__":
    class TestActor(Actor):
        def receive(self, message):
            print "this is test actor: ", message, id(self)

        def handle_TestMessage(self, msg):
            print "test message: ", msg

        def handle_IoMessage(self, msg):
            print "io message: ", msg

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
    test.inbox.put("bu nesne Message class'ından türetilmedi")

    test.send("naber")

    gevent.sleep(100)