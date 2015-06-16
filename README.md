#Distributed Control System Library for Python

Gevent based actor model (inspired from Erlang) used for concurrency. API is heavily inspired from [pysage](https://github.com/realtime-system/pysage).  


### Actors in the same process

Testing actor model in the same process:

```
python pinger_ponger.py
```

### Actors distributed in the same machine

pinger.py: 
```py
from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Pinger(Actor):
    def handle_PingMessage(self, msg):
        print "Pinger got ping message: ", msg.text
        sleep(5)
        self.send(PongMessage(text="Hello ponger!"))


if __name__ == "__main__":
    ProxyActor()
    pinger = Pinger()
    pinger.send(PongMessage(text="startup message from pinger..."))
    pinger.join()
```

On the first terminal, run `pinger.py`: 
```
$ python pinger.py
```

---

ponger.py:
```py
from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg.text
        sleep(5)
        self.send(PingMessage(text="Hello pinger!"))

if __name__ == "__main__":
    ProxyActor()
    ponger = Ponger()
    ponger.send(PingMessage(text="startup message from ponger..."))
    ponger.join()
```

On the second terminal, run `ponger.py`: 

```
$ python ponger.py
```

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
