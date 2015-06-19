#Distributed Control System Library for Python

Gevent based actor model (inspired from Erlang) used for concurrency. API is heavily inspired from [pysage](https://github.com/realtime-system/pysage).  

aktos-dcs uses "addressing broker" to solve "dynamic service discovery" problem. The 'addressing broker' is created, watched for failures and recreated dynamically by alive actors. 

### Actors in the same process

Actor model in the same process:

```
$ python pinger_ponger.py
```

### Actors distributed in the same machine

On the first terminal, run `pinger.py`: 
```
$ python pinger.py
```

On the second terminal, run `ponger.py`: 

```
$ python ponger.py
```

On the third terminal, run `pinger2.py`:

```
$ python pinger2.py
```

and so on... 

### Actors distributed on the Local Area Network

First, run above examples in a machine. On the other machine, 

* open `pinger-remote.py` 
* edit `broker_host` parameter of `ProxyActor()`
* run `pinger-remote.py`
* likewise, edit and run `ponger-remote.py`


### Platforms

Should work on any platform, tested on:

* Windows (XP)
* Linux (Debian, Ubuntu, Raspbian)

### Install 

This library depends on Gevent 1.0.2 and ZeroMQ 14.6.0 or later.

if windows: download and install http://aka.ms/vcpython27 first; then: 

```
# easy_install pyzmq gevent
```

### License

BSD License. 

### Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey
info@aktos-elektronik.com
https://aktos-elektronik.com

### TODO:

* Prepare documentation
* Make a complete TODO list 
