#Distributed Control System Library for Python

Gevent based actor model (inspired from Erlang) used for concurrency. API is heavily inspired from [pysage](https://github.com/realtime-system/pysage).  


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

### Dependencies

* Platforms: Any
* Tested on: Windows, Linux

```
# easy_install pyzmq gevent
```
### Status

Status is alpha (neither completed, nor heavily tested) for now. Contributions are welcome. 

### TODO:

* Make a TODO list 
* Prepare documentation
