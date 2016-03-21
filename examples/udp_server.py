from aktos_dcs import *


print('Receiving datagrams on :9000')
UdpServer(':9000').serve_forever()

