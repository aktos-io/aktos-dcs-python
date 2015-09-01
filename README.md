#Python bindings for Distributed Control System Library

**aktos_dcs** is designed for creating **fault tolerant**, **realtime**, **massively concurrent**, **distributed** (even behind firewalls), **io-bound** (eg. heavy-traffic web server), **scalable** (both vertically and horizontally), **cross-platform** and **language agnostic** applications.

This library is developed for distributed automation projects in mind. Any PLC or motion controller related work (including [HMI and SCADA](https://en.wikipedia.org/wiki/SCADA)) can be performed easily. Simulation of a real component of the target system becomes a trivial work to do. Graphical User Interface can be built by using desktop and mobile frameworks (Qt, GTK, ...) or by web technologies (HTML5, Javascript, CSS, ...). 

Message transport layer is built on top of ZeroMQ library, which has [Python][4], [Java][2], [Node.js][5], [C][3], [C++][6] , [C#][1] and [many other bindings][7]. This means, any number of these languages can be used together to build a single project. Developers can work with their favourite language. 

[1]: https://github.com/zeromq/netmq
[2]: https://github.com/zeromq/jzmq
[3]: https://github.com/zeromq/czmq
[4]: https://github.com/zeromq/pyzmq
[5]: https://github.com/JustinTulloss/zeromq.node
[6]: https://github.com/zeromq/cppzmq
[7]: http://zeromq.org/bindings:_start

Gevent based actor model (inspired from Erlang) is used for concurrency. This means, concurrency comes for free. Since there are no real threads or subprocesses, debugging is easy. N-to-N connections are managed out of the box, so there is no single point of failure exists. 

For a short tutorial, see `TESTS.md`. 

## Other Examples

1. Serial port usage example: https://github.com/ceremcem/aktos-dcs-pyserial-example
2. WEB UI example: https://github.com/ceremcem/aktos-dcs-webui-example
3. aktos-dcs-lib-cca: https://github.com/ceremcem/aktos-dcs-lib-cca
4. aktos-website: https://github.com/ceremcem/aktos-website

## Other Implementations

1. Java: https://github.com/Canburakt/aktos-dcs-java
2. Node.js (in LiveScript): https://github.com/ceremcem/aktos-website/blob/master/app/aktos-dcs.ls

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

This library depends on `gevent 1.x`, `libzmq 4.x`, `netifaces`, `ujson`

#### Windows: 

* install [Python 2.7.x](https://www.python.org/downloads/)
* install http://aka.ms/vcpython27
* clone or download aktos-dcs
* run (double click on) "aktos-dcs\\install-on-windows.cmd 

#### Linux:

* clone or download aktos-dcs
* `$ cd aktos-dcs && sudo install-on-linux.sh` (compilations may take about 3-5 minutes)

## Message Format

Messages are simple dictionaries, represented in JSON format. Mandatory keys of a message are as follows: 

  * sender: Array of strings. First element is creator's, rest is forwarder's `id`'s.
  * timestamp: Unix timestamp (seconds since 1.1.1970)
  * msg_id: a unique message id. practically concatenate `creator_id` and `i` where `i` is sequence number of message
  * payload: a dictionary, described below. 

Payload is basically in `{'Subject': data}` format. Here are some examples: 
  
  * To set `green-led` pin to `True`, one must send the following message: 
  
    Python: 
    
        msg = { 'IoMessage': { 'pin_name': 'green-led', 'val': True } }
              
    Javascript: 
    
        var msg = { IoMessage: { pin_name: 'green-led', val: true } }
  
    LiveScript:
    
        msg = IoMessage: pin_name: \green-led, val: on

        or 
        
        msg = IoMessage: 
               pin_name: \green-led
               val: on 
          
    
So, a full message should look like this:

    {"sender":["5fa6c6d7-077a-4467-9bb3-1f2c2ee58d78","5e7b8786-4885-4e2d-b4c6-98dc21856ba9","3444aadc-ed01-4ce6-94bc-ae144510eb31","41dl-Gj3"],"timestamp":1440885632.49,"msg_id":"5fa6c6d7-077a-4467-9bb3-1f2c2ee58d78.147","payload":{"IoMessage":{"pin_name":"green-led","val":true}}}

## License

BSD License. 

## Contact and Support

A.K.T.O.S. Electronics, the Open Source Telemetry and Automation Systems company, Turkey

info@aktos-elektronik.com

https://aktos-elektronik.com
