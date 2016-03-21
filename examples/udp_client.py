from aktos_dcs import *

def on_receive(data):
    print "received: ", data

x = UdpClient(host="192.168.2.107", port=5011, receiver=on_receive)


try:
    print "Started sending..."
    i = 0
    while True:
        msg = "Hello, I'm udp message (%d)" % i
        print "sending: " + msg
        x.socket_write(msg + "\n")
        i += 1
        sleep(1)
except:
    print "cleaning up..."
    x.cleanup()


