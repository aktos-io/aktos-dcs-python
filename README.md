#Distributed Control System Library for Python

Gevent based actor model (inspired from Erlang) used for concurrency. API is heavily inspired from [pysage](https://github.com/realtime-system/pysage).  

aktos-dcs uses "addressing broker" to solve "dynamic service discovery" problem. The 'addressing broker' is created and destroyed dynamically by joiner actors upon demand. 


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



### Platforms

Should work on any platform, tested on:

* Windows XP
* Linux (Debian, Ubuntu)

### Install 

This library depends on Gevent 1.0.2 and ZeroMQ 14.6.0 or later.

if windows: download and install http://aka.ms/vcpython27 first; then: 

```
# easy_install pyzmq gevent
```
### Status

Status is alpha (neither completed, nor heavily tested) for now. Contributions are welcome. 

### TODO:

* Make a TODO list 
* Prepare documentation
