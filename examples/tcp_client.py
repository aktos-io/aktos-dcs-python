from aktos_dcs import *

def on_receive(data):
    print "received: ", data

#x = TcpClient(host="192.168.2.186", port=23, receiver=on_receive)
x = TcpClient(host="192.168.2.107", port=22334, receiver=on_receive)


try:
    print "Started sending..."
    i = 0
    while True:
        msg = "hello, I'm tcp client! (%d)" % i
        print "sending: ", msg
        x.socket_write(msg + "\n")
        i += 1
        sleep(1)
except:
    print "cleaning up..."
    x.cleanup()


