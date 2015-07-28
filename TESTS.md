1. Messages could run tests without error.

    * run `python aktos_dcs/cca_messages.py`
    * see "all went OK" message.

2. pinger.py and ponger.py should run on the same machine without giving any `brokers` or `proxy_brokers` parameters.

    * run pinger.py
    * run ponger.py
    * see they are messaging

3. pinger.py and ponger.py should change their "address broker" role at any time.

    * run pinger.py (this will create broker)
    * run ponger.py
    * see they are messaging
    * kill pinger.py
    * see ponger.py creates broker
    * run pinger.py
    * see they are messaging

4. different machines should ping-pong.

    * run pinger.py on machine A
    * edit ponger.py on machine B and give `brokers='IP_OF_MACHINE_A:5012:5013'` parameter
    * run ponger.py on machine B
    * see they are messaging

5. connection should be established even if machine A kills its broker

    * run test#4
    * kill pinger.py on machine A
    * see they are not messaging anymore
    * run pinger.py on machine A
    * see they are started messaging again.

6. inherit current contact_list

    * run test#5
    * run foo.py on machine A (without ProxyActor parameter)
    * run bar.py on machine B (without ProxyActor parameter)
    * see foo.py and bar.py can message eachother.

7. detect multiple local IP addresses but prevent from duplicate messages

    * setup additional addresses to machine A and machine B
    * see you have more than 1 address on machine
    * see you could ping machine A to B and B to A via each of their addresses
    * run test#6
    * see messages are the same as in test#6






