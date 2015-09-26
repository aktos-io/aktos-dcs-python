import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Ponger(Actor):
    def action(self):
        self.max_latency = 0
        self.min_latency = 9999

    def handle_PongMessage(self, msg):
        body = get_msg_body(msg)
        latency = time.time() - msg['timestamp']
        if self.max_latency < latency:
            self.max_latency = latency
            print "latency (max, min): ", self.max_latency, self.min_latency

        if self.min_latency > latency:
            self.min_latency = latency
            print "latency (max, min): ", self.max_latency, self.min_latency

        sleep(0.01)
        self.send({'PingMessage': {'text': "Hello pinger, this is ponger 1!"}})

if __name__ == "__main__":
    ProxyActor()
    #ProxyActor(brokers="192.168.2.119:5012:5013", proxy_brokers="localhost:8012:8013")
    #ProxyActor(brokers="192.168.1.3:5012:5013")
    ponger = Ponger()
    ponger.send({'PingMessage': {'text': "Hello pinger, STARTUP MESSAGE!"}})

    wait_all()
