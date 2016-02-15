from aktos_dcs import * 

class TestBarrier(Actor):
    def action(self):
        self.b = Barrier()
        while True: 
            print "waiting for barrier to open..."
            self.b.wait()
            print "barrier is opened, continuing..."
            sleep(2)

    def handle_BarrierMessage(self, msg):
        print "handler is opening the barrier"
        self.b.go()


class Test2(Actor):
    def action(self):
        while True:
            print "sending 'open barrier' message"
            self.send({'BarrierMessage': {}})
            sleep(2)

print "starting application"
TestBarrier()
Test2()
wait_all()
