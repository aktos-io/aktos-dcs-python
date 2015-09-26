import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *


class Ponger(Actor):
    def handle_PongMessage(self, msg):
        msg = get_msg_body(msg)
        print "Pong got pong message:", msg['text']
        print "ponger is started to wait", time.time()
        sleep(2)
        #self.send({'PingMessage': {'text': "Hello pinger!"}})
        print "ponger has done waiting", time.time()


class Pinger(Actor):
    def action(self):
        print "pinger is sending msg", time.time()
        self.ask({'PongMessage': {'text': "Hello pinger!"}}, to='foo')
        print "pinger is continuing", time.time()



if __name__ == "__main__":
    Pinger()
    Ponger(name="foo")
    wait_all()
