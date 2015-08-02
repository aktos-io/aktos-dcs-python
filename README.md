#Python bindings for Distributed Control System Library

**aktos_dcs** is a library for creating massively concurrent, distributed (even behind firewalls), io-bound (eg. heavy-traffic-web-server), vertically and horizontally scalable, cross-platform and language agnostic applications.

Message transport layer is built on top of ZeroMQ library, which has [Python][4], [Java][2], [Node.js][5], [C][3], [C++][6] , [C#][1] and [many other bindings][7]. This means, any number of these languages can be used together to build a single project. Developers can work with their favourite language. 

[1]: https://github.com/zeromq/netmq
[2]: https://github.com/zeromq/jzmq
[3]: https://github.com/zeromq/czmq
[4]: https://github.com/zeromq/pyzmq
[5]: https://github.com/JustinTulloss/zeromq.node
[6]: https://github.com/zeromq/cppzmq
[7]: http://zeromq.org/bindings:_start

Gevent based actor model (inspired from Erlang) used for concurrency. This means, concurrency is [nearly] for free. Since there is no real threads or subprocesses, debugging is easy. N-to-N connections are managed out of the box, so there is no single point of failure exists. 

For a short tutorial, see `TESTS.md`. 

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

## Install 

This library depends on `gevent 1.x`, `libzmq 4.x`, `netifaces`

#### Windows: 

* install [Python 2.7.x](https://www.python.org/downloads/release/python-279/)
* install http://aka.ms/vcpython27
* download and run "[windows-install-deps.cmd](https://raw.githubusercontent.com/ceremcem/aktos-dcs/master/windows-install-deps.cmd)" (right click, "save as...", download, double click on it) 
* install `gevent` from: https://code.google.com/p/gevent/downloads/detail?name=gevent-1.0b4.win32-py2.7.msi&can=1&q=

#### Linux:

* `$ sudo apt-get install python-dev`
* `$ sudo easy_install simplejson pyzmq gevent netifaces` (compilations take about 3-5 minutes)

## License

BSD License. 

## Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey

info@aktos-elektronik.com

https://aktos-elektronik.com
