#Distributed Control System Library for Python

*aktos_dcs* is a library for creating massively concurrent, distributed (even behind firewalls), io-bound (eg. web servers with heavy traffics), vertically and horizontally scalable and cross-platform applications. 

Gevent based actor model (inspired from Erlang) used for concurrency. Messaging layer is heavily inspired from [pysage](https://github.com/realtime-system/pysage).  

For a short tutorial, see `TESTS.md`. 

### Distributed coding

Actors can be run concurrently

* in the same process
* in the same machine (can take advantage of multiple CPU cores)
* distributed in Local Area Network
* distributed across networks and connected via proxies/tunnels (eg. ssh tunnel)

### Platforms

Should work on any platform, tested on:

* Windows (XP, 7, 8.1)
* Linux (Debian, Ubuntu, Raspbian)

### Install 

This library depends on `gevent 1.x`, `libzmq 4.x`, `netifaces`

#### Windows: 

* install [Python 2.7.x](https://www.python.org/downloads/release/python-279/)
* install http://aka.ms/vcpython27
* `C:\Python27\Scripts>easy_install simplejson pyzmq greenlet netifaces`
* install `gevent` from: https://code.google.com/p/gevent/downloads/detail?name=gevent-1.0b4.win32-py2.7.msi&can=1&q=

#### Linux:

* `$ sudo apt-get install python-dev`
* `$ sudo easy_install simplejson pyzmq gevent netifaces` (compilations take about 3-5 minutes)

### License

BSD License. 

### Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey

info@aktos-elektronik.com

https://aktos-elektronik.com
