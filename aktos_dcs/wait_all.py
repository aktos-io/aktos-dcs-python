__author__ = 'ceremcem'

import gevent

def wait_all():
    while True:
        gevent.sleep(1)