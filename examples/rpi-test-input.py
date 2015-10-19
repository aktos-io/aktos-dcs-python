import add_import_path # only for examples

from aktos_dcs import *
from aktos_dcs_lib import *
if __name__ == "__main__":
    gpio_list = [i for i in range(2, 27)]

    input_pins = {}
    for i in gpio_list: 
        input_pins['gpio.%d' % i] = i

    for k, v in input_pins.items():
        GPIOInputActor(pin_name=k, pin_number=v, invert=True)

    wait_all()

