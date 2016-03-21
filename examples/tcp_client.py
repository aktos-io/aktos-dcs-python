from aktos_dcs import *

def on_receive(data):
    print "received: ", data

#x = TcpClient(host="192.168.2.186", port=23, receiver=on_receive)
x = TcpClient(host="localhost", port=22334, receiver=on_receive)


try:
    print "Started sending..."
    while True:
        x.socket_write("x"*50 + "\n")
        sleep(1)
except:
    print "cleaning up..."
    x.cleanup()


