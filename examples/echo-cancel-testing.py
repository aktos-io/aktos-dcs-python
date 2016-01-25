import add_import_path # only for examples

from aktos_dcs import *

class Pinger(Actor):
    def action(self): 
        while True: 
            print "sending ping message..."
            self.send({'PingMessage': {'text': "Hello ponger, this is pinger 1!"}})
            sleep(1)
            
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg['text']


class Test(Actor): 
    def handle_PingMessage(self, msg): 
        print "Test got message: ", msg["text"]
        self.send({'PingMessage': {'text': "This is test actor!"}})
        

if __name__ == "__main__":
    """
    An actor can not receive a message that he sends. 

    For example, if Test actor wasn't replying the PingMessage, Pinger actor 
    would not be able to print "Pinger got ping message". 
    """
    Pinger()
    Test()
    wait_all()
