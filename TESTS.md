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

    * run test 4
    * kill pinger.py on machine A
    * see they are not messaging anymore
    * run pinger.py on machine A
    * see they are started messaging again.

6.

