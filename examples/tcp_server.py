from aktos_dcs import *


class TestHandler(TcpHandlerActor):

    def on_connect(self):
        print "there is a connection!", self.client_id

    def on_disconnect(self):
        print "client disconnected: ", self.client_id

    def socket_read(self, data):
        print "I got following data: ", data

    def action(self):
        i = 0
        while True:
            print "sending test data..."
            self.socket_write("naber... (%d)\n" % i)
            i += 1
            sleep(2)

print "Started TcpServer on port 22334"
#TcpServerActor(address='0.0.0.0', port=22334)
TcpServerActor(address='0.0.0.0', port=22334, handler=TestHandler)
wait_all()
