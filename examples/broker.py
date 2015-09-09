import add_import_path # only for examples
__author__ = 'ceremcem'

from aktos_dcs import *

if __name__ == "__main__":
    ProxyActor(brokers="10.0.10.176:5012:5013")
    wait_all()
