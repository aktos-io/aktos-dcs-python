from aktos_dcs import *

def on_receive(data):
    print "received: ", data

x = UdpClient(host="localhost", port=5011, receiver=on_receive)


try:
    print "Started sending..."
    while True:
        x.socket_write("x"*50 + "\n")
        sleep(1)
except:
    print "cleaning up..."
    x.cleanup()


