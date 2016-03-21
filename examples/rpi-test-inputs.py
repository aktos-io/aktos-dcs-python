from aktos_dcs import *


if __name__ == "__main__":
    input_pins = {
        'test-input-0': 6,
        'test-input-1': 5,
        'test-input-2': 13,
        'test-input-3': 19,
        'test-input-4': 16,
        'test-input-5': 26,
        'test-input-6': 20,
        'test-input-7': 21,
    }

    for k, v in input_pins.items():
        GPIOInputActor(pin_name=k, pin_number=v, invert=True)

    ProxyActor()
    wait_all()

