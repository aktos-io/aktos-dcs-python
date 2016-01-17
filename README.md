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

## Platforms

Should work on any platform, tested on:

* Windows (XP, 7, 8.1)
* Linux (Debian, Ubuntu, Raspbian)
* Os X (El capitan tested) 

## Examples

1. [TESTS.md](./TESTS.md) can be considered as a short tutorial. 
2. Serial port usage example: https://github.com/ceremcem/aktos-dcs-pyserial-example
3. aktos-dcs-lib: https://github.com/ceremcem/aktos-dcs-lib
4. aktos-scada as the SCADA and HMI infrastructure: https://github.com/ceremcem/aktos-scada
5. Qt desktop application: https://github.com/ceremcem/weighing-machine-testing

## Other Implementations

1. Java: https://github.com/Canburakt/aktos-dcs-java
2. Node.js (in LiveScript): https://github.com/ceremcem/aktos-website/tree/master/app/modules/aktos-dcs
3. C#: https://github.com/ceremcem/aktos-dcs-cs

## Recommended Tools and Libraries

* https://github.com/ceremcem/aktos-dcs-tools : for easy remote development 
* https://github.com/ceremcem/link-with-server : for easy proxy connection of iot devices
* https://github.com/ceremcem/aktos-dcs-lib: library for automation projects 
* https://github.com/ceremcem/aktos-scada: Web based SCADA system which is live at https://aktos-elektronik.com

## Install 

Compilations may take around 3 minutes. 

#### Windows: 

* install [Python 2.7.x](https://www.python.org/downloads/)
* install http://aka.ms/vcpython27
* clone or download aktos-dcs
* run (double click on) "`aktos-dcs\`[install-on-windows.cmd](./install-on-windows.cmd) 

#### Linux:

* clone or download aktos-dcs
* `$ cd aktos-dcs && sudo `[install-on-linux.sh](./install-on-linux.sh) 


#### Os X - El Capitan:

* Requires [homebrew](http://brew.sh/) if it's not installed already. 
* clone or download aktos-dcs
* `$ cd aktos-dcs && sudo `[install-on-osx.sh](./install-on-osx.sh) 

## Guides for further implementations

See:  [Developer Guide](./Developer-guide.md)

## Similar Projects

* Crossbar.io: https://github.com/crossbario

## License

BSD License. 

## Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey

info@aktos-elektronik.com

https://aktos-elektronik.com
