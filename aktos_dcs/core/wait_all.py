__author__ = 'ceremcem'

import gevent

def wait_all():
    while True:
        try:
            gevent.sleep(9999999999)
        except:
            break
