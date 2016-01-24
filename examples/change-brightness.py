import add_import_path # only for examples

from aktos_dcs import *

class Test(Actor):
    def handle_IoMessage(self, msg):
        if msg["pin_name"] == "izmirhs-brightness":
            with open("/sys/class/backlight/radeon_bl0/brightness", 'w') as f:
                f.write(msg["val"])

        print("Got message: %s", msg["val"])


if __name__ == "__main__":
    ProxyActor(brokers="192.168.2.155:5012:5013")
    Test()
    wait_all()
