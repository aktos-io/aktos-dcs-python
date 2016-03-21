from aktos_dcs import *

gpio_list = [i for i in range(2, 27)]

input_pins = {}
for i in gpio_list:
    input_pins['gpio.%d' % i] = i

for k, v in input_pins.items():
    GPIOInputActor(pin_name=k, pin_number=v, invert=True)

wait_all()

