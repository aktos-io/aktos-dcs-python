from aktos_dcs import *


print('Receiving datagrams on :5011')
UdpServerActor(address='0.0.0.0', port=5011)
print "waiting..."
wait_all()


