#Python bindings for Distributed Control System Library 

**aktos_dcs** is designed for creating **fault tolerant**, **realtime**, **massively concurrent**, **distributed** (even behind firewalls), **io-bound** (eg. heavy-traffic web server), **scalable** (both vertically and horizontally), **cross-platform** and **language agnostic** applications.

This library is developed for distributed automation projects in mind. Any PLC or motion controller related work (including [HMI and SCADA](https://github.com/ceremcem/aktos-scada)) can be performed easily. Simulation of a real component of the target system becomes a trivial work to do. Graphical User Interface can be built by using desktop and mobile frameworks (Qt, GTK, ...) or by web technologies (HTML5, Javascript, CSS, ...). 

Message transport layer is built on top of ZeroMQ library, which has [Python][4], [Java][2], [Node.js][5], [C][3], [C++][6] , [C#][1] and [many other bindings][7]. This means, any number of these languages can be used together to build a single project. Developers can work with their favourite language. 

[1]: https://github.com/zeromq/netmq
[2]: https://github.com/zeromq/jzmq
[3]: https://github.com/zeromq/czmq
[4]: https://github.com/zeromq/pyzmq
[5]: https://github.com/JustinTulloss/zeromq.node
[6]: https://github.com/zeromq/cppzmq
[7]: http://zeromq.org/bindings:_start

Gevent based actor model (inspired from Erlang) is used for concurrency. This means, [concurrency comes for free](http://www.projectcalico.org/the-sharp-edges-of-gevent/). Since there are no real threads or subprocesses, debugging is easy. N-to-N connections are managed out of the box, so there is no single point of failure exists. 

## Distributed coding

Actors can be run concurrently

* in the same process
* in the same machine (can take advantage of multiple CPU cores)
* distributed in Local Area Network
* distributed across networks and connected via proxies/tunnels (eg. ssh tunnel)

## Sample Code

This is [`pinger.py`](./examples/pinger.py)

```py
from aktos_dcs import *

class Pinger(Actor):
    def action(self):
        self.send_PongMessage(text="Hello ponger, this is STARTUP MESSAGE!")

    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg['text']
        sleep(2)
        self.send_PongMessage(text="Hello ponger, this is pinger1!")

ProxyActor()
Pinger()
wait_all()
```

This is [`ponger.py`](./examples/ponger.py)

```py
from aktos_dcs import *


class Ponger(Actor):
    def action(self):
        self.send_PingMessage(text="Hello pinger, this is STARTUP MESSAGE!")

    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg['text']
        sleep(2)
        self.send_PingMessage(text="Hello pinger, this is ponger 1!")

ProxyActor(brokers="192.168.2.161:5012:5013")
Ponger()
wait_all()
```

These two programs can interact with eachother even they are in the same file (like [`pinger_ponger.py`](./examples/pinger_ponger.py), or they are separate processes running in the same machine (where they are taking advantage of multiple CPU cores) or they are on separate machines on the LAN (where `pinger.py` runs on a machine "192.168.2.161").

## Platforms

Should work on any platform, tested on:

* Windows (XP, 7, 8.1)
* Linux (Debian, Ubuntu, Raspbian)
* Os X (El capitan tested) 

## Examples

1. [Test README](./test/README.md) can be considered as a short tutorial. 
2. Examples can be found in [examples](./examples) directory
4. aktos-scada as the SCADA and HMI infrastructure: https://github.com/aktos-io/aktos-scada
5. Qt desktop application: https://github.com/ceremcem/weighing-machine-testing

## Other Implementations

1. C#: https://github.com/aktos-io/aktos-dcs-cs
2. Node.js (in LiveScript): https://github.com/aktos-io/aktos-scada/tree/master/app/modules/aktos-dcs
3. Java: https://github.com/Canburakt/aktos-dcs-java

## Recommended Tools and Libraries

* https://github.com/aktos-io/aktos-dcs-tools : for easy remote development 
* https://github.com/aktos-io/link-with-server : for easy proxy connection of iot devices

## Install 

See [Install README](./install/README.md)

## Update 

Run `update-aktos-dcs` in terminal whenever you need. 

## Guides for further implementations

See:  [Developer Guide](./doc/Developer-guide.md)

## Similar Projects

* Crossbar.io: https://github.com/crossbario

## License

BSD License. 

## Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey

info@aktos.io

https://aktos.io
