#Distributed Control System Library for Python

### Dependencies

Platforms: Any
Tested on: Windows, Linux

```
# easy_install pyzmq
```

### Actors in the same process

Testing actor model in the same process:

```
python pinger_ponger.py
```

### Actors distributed in the same machine
Testing actor model on the same machine: 

On the first terminal: 

```
$ python pinger.py
```

On the second terminal: 

```
$ python ponger.py
```
