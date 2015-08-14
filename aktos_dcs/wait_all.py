__author__ = 'ceremcem'

import gevent

def wait_all():
    try:
        while True:
            gevent.sleep(1)
    except:
        pass