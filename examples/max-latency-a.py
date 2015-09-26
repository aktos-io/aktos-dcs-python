import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

class Pinger(Actor):
    def action(self):
        self.max_latency = 0
        self.min_latency = 9999

    def handle_PingMessage(self, msg):
        body = get_msg_body(msg)
        latency = time.time() - msg['timestamp']
        if self.max_latency < latency:
            self.max_latency = latency
            print "latency (max, min): ", self.max_latency, self.min_latency

        if self.min_latency > latency:
            self.min_latency = latency
            print "latency (max, min): ", self.max_latency, self.min_latency

        #print "naber", body
        sleep(0.001)
        self.send({'PongMessage': {'text': "Hello ponger, this is pinger 1!"}})

if __name__ == "__main__":
    try:
        #import GreenletProfiler
        #GreenletProfiler.set_clock_type('cpu')
        #GreenletProfiler.start()
        ProxyActor()
        pinger = Pinger()
        pinger.send({'PongMessage': {'text': "Hello ponger, this is STARTUP MESSAGE!"}})

        wait_all()
    except:
        #GreenletProfiler.stop()
        #stats = GreenletProfiler.get_func_stats()
        #stats.print_all()
        pass

