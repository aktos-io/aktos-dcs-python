1. Messages could run tests without error.

    * run `python aktos_dcs/cca_messages.py`
    * see "all went OK" message.

2. Pinger and Ponger should run in the same process without error.

    * run pinger_ponger.py
    * see it works

3. pinger.py and ponger.py should run on the same machine without giving any `brokers` or `proxy_brokers` parameters.

    * run pinger.py
    * run ponger.py
    * see they are messaging

4. pinger.py and ponger.py should change their "address broker" role at any time.

    * run pinger.py (this will create broker)
    * run ponger.py
    * see they are messaging
    * kill pinger.py
    * see ponger.py creates broker
    * run pinger.py
    * see they are messaging

5. {{LAN-test-1}} different machines should ping-pong.

    * run pinger.py on machine-A
    * edit ponger.py on machine-B and give `brokers='IP-OF-MACHINE-A:5012:5013'` parameter
    * run ponger.py on machine-B
    * see they are messaging

6. {{LAN-test-2}} connection should be established even if machine A kills its broker

    * run {{LAN-test-1}}
    * kill pinger.py on machine-A
    * see they are not messaging anymore
    * run pinger.py on machine-A
    * see they are started messaging again.

6. {{LAN-test-3}} inherit current contact_list

    * run {{LAN-test-2}}
    * run foo.py on machine-A (without ProxyActor parameter)
    * run bar.py on machine-B (without ProxyActor parameter)
    * see foo.py and bar.py can message eachother.

7. {{LAN-test-4}} detect multiple local IP addresses but prevent from duplicate messages

    * setup additional addresses to machine-A and machine-B
    * see you have more than 1 address on machine
    * see you could ping machine-A to machine-B and machine-B to machine-A via each of their addresses
    * run {{LAN-test-3}}
    * see messages are the same as in {{LAN-test-3}}

8. {{proxy-test-1}} test if processes connect behind NAT

    * setup machine-A behind NAT with SSH server or standard modem port forward
    * run pinger.py on machine-A
    * forward broker ports (5012 and 5013) from machine-A to machine-B via SSH

        machine-B:$ ssh user@machine-A -L 8012:localhost:5012 8013:localhost:5013

    * run ponger.py with at least `ProxyActor(proxy_brokers="localhost:8012:8013")` parameter on machine-B
    * see ping-pong occurs.
    * kill pinger.py on machine-A
    * wait couple of seconds.
    * start pinger.py on machine-A again
    * see they are messaging

9. {{proxy-test-2}} test if multiple processes can use same tunnel

    * run {{proxy-test-1}}
    * run foo.py on machine-A without any parameter of ProxyActor
    * see foo.py connects to pinger.py (they are in the same machine)
    * run bar.py on machine-B without any parameter of ProxyActor
    * see bar.py connects (and exchanges contact-list) with ponger.py (they are in the same machine)
    * see foo.py and bar.py are messaging

10. {{proxy-test-3}} test if a machine that can reach another with tunnels is also
    proxies messages via another machine in LAN

    * setup machine-C that is in the same LAN with machine-B
    * run {{proxy-test-2}}
    * kill bar.py on machine-B
    * ensure that bar.py on machine-C has `brokers="ip-of-machine-B:5012:5013"` parameter in the ProxyActor
    * run bar.py on machine-C
    * see if bar.py@machine-C and foo.py@machine-A are messaging






