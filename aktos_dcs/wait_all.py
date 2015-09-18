__author__ = 'ceremcem'

import gevent

def wait_all():
    try:
        while True:
            gevent.sleep(9999999999)
    except:
        pass