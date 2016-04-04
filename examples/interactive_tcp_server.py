__author__ = 'ceremcem'
from aktos_dcs import *


class TestHandler(TcpHandlerActor):
    def prepare(self):
        self.io_prompt = IoPrompt()
        self.io_prompt.send_cmd = lambda x: self.socket_write(x + "\n")
        self.io_prompt.start_io_prompt()

    def on_connect(self):
        print "there is a connection!", self.client_id

    def socket_read(self, data):
        self.io_prompt.prompt_read(data)


PORT=1235
print "Tcp Server is running on *:%d" % PORT
TcpServerActor(address='0.0.0.0', port=PORT, handler=TestHandler)
wait_all()
